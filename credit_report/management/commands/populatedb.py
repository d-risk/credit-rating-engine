import urllib.request
from datetime import datetime, timezone
from random import choice, uniform, random, randrange
from typing import Tuple, List

from django.core.management.base import BaseCommand

from credit_report.models import Company, CreditRating, Report, RiskDriver, Unit

AMOUNT = 'amount'


def create_credit_rating(
        score: int = 1, text: str = choice(['A', 'B', 'C']), date: datetime = datetime.now(timezone.utc),
) -> CreditRating:
    credit_rating = CreditRating(
        score=score,
        text=text,
        date=date,
    )
    credit_rating.save()
    return credit_rating


def create_risk_driver(
        name: str, unit: Unit = Unit.UNKNOWN,
        latest: float = None, maximum: float = None, minimum: float = None, average: float = None,
) -> RiskDriver:
    risk_driver = RiskDriver(
        name=name,
        unit=unit,
        latest=latest if latest else random_value(unit),
        maximum=maximum if maximum else random_value(unit),
        minimum=minimum if minimum else random_value(unit),
        average=average if average else random_value(unit),
    )
    return risk_driver


def random_value(unit: Unit) -> float:
    value = 1
    if unit is Unit.PERCENTAGE:
        value = random()
    elif unit is Unit.MULTIPLICATIVE:
        value = uniform(0, 1000)
    elif unit is Unit.UNKNOWN:
        value = randrange(999_999_999_999)
    return value


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(AMOUNT, type=int)

    def handle(self, *args, **options):
        self.create_singtel()
        self.create_companies(options[AMOUNT], 2015, 2018)

    def create_singtel(self):
        company, created = self.create_company(
            name='Singapore Telecommunications Limited',
            description='Singapore Telecommunications Limited provides integrated infocomm technology solutions to enterprise customers primarily in Singapore, Australia, the United States of America, and Europe. The company operates through Group Consumer, Group Enterprise, and Group Digital Life segments. The Group Consumer segment is involved in carriage business, including mobile, pay TV, fixed broadband, and voice, as well as equipment sales. The Group Enterprise segment offers mobile, equipment sales, fixed voice and data, managed services, cloud computing, cyber security, and IT and professional consulting services. The Group Digital Life segment engages in digital marketing, regional video, and advanced analytics and intelligence businesses. The company also operates a venture capital fund that focuses its investments on technologies and solutions. Singapore Telecommunications Limited is headquartered in Singapore.',
            industry='Telecommunications',
        )
        if created:
            self.create_rating(
                company=company,
                credit_rating=create_credit_rating(text='A1'),
                risk_drivers=[
                    create_risk_driver('Profitability', Unit.PERCENTAGE, latest=5.7, maximum=7.7,
                                       minimum=5.7,
                                       average=6.7),
                    create_risk_driver('Debt Coverage', Unit.MULTIPLICATIVE, latest=76.2, maximum=81.2,
                                       minimum=70.4,
                                       average=75.8),
                    create_risk_driver('Leverage', Unit.PERCENTAGE, latest=40.5, maximum=41.5, minimum=37.7,
                                       average=39.6),
                    create_risk_driver('Liquidity', Unit.PERCENTAGE, latest=1.11, maximum=1.58, minimum=1.06,
                                       average=1.32),
                    create_risk_driver('Size', Unit.UNKNOWN, latest=48_294_200, maximum=48_294_200,
                                       minimum=39_320_000,
                                       average=43_807_100),
                    create_risk_driver('Country Risk', Unit.UNKNOWN, latest=1, maximum=1, minimum=1,
                                       average=1),
                    create_risk_driver('Industry Risk', Unit.UNKNOWN, latest=1, maximum=1, minimum=1,
                                       average=1),
                    create_risk_driver('Competitiveness', Unit.UNKNOWN, latest=1, maximum=1, minimum=1,
                                       average=1),
                ],
            )

    def create_companies(self, amount: int, from_year: int, to_year: int):
        companies = []
        with urllib.request.urlopen('http://www.desiquintans.com/downloads/nounlist/nounlist.txt') as response:
            nouns = response.read().decode().splitlines()
            self.stdout.write(f'Using {len(nouns)} nouns to create {amount} companies:')
            for i in range(amount):
                company, created = self.create_company(name=f'{choice(nouns)} {choice(nouns)} {choice(nouns)}')
                if created:
                    companies.append(company)
                    ratios = [
                        ('Profitability', Unit.PERCENTAGE),
                        ('Debt Coverage', Unit.MULTIPLICATIVE),
                        ('Leverage', Unit.PERCENTAGE),
                        ('Liquidity', Unit.PERCENTAGE),
                        ('Size', Unit.UNKNOWN),
                        ('Country Risk', Unit.UNKNOWN),
                        ('Industry Risk', Unit.UNKNOWN),
                        ('Competitiveness', Unit.UNKNOWN),
                    ]
                    for year in range(from_year, to_year + 1):
                        self.create_rating(
                            company=company,
                            credit_rating=create_credit_rating(
                                date=datetime(year=year, month=1, day=1, tzinfo=timezone.utc),
                            ),
                            risk_drivers=[create_risk_driver(name, unit) for name, unit in ratios],
                        )
        self.stdout.write(f'{len(companies)} companies created, {amount - len(companies)} duplicates')

    def create_company(self, name: str, description: str = '', industry: str = '') -> Tuple[Company, bool]:
        company, created = Company.objects.get_or_create(
            defaults={
                'description': description,
                'industry': industry,
            },
            name=name,
        )
        s = 'created' if created else 'already exists'
        self.stdout.write(f'    + Company \'{company.name}\' ({company.id}) {s}')
        return company, created

    def create_rating(
            self,
            company: Company,
            credit_rating: CreditRating,
            risk_drivers: List[RiskDriver],
    ) -> Report:
        report = Report(
            company_id=company.id,
            credit_rating=credit_rating,
        )
        report.save()
        report.risk_drivers.set(risk_drivers, bulk=False)
        self.stdout.write(f'        + Rating \'{report.id}\' ({report.credit_rating.date}) created')
        return report
