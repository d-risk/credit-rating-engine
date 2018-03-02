import urllib.request
from datetime import datetime, timezone
from random import choice
from typing import Tuple

from django.core.management.base import BaseCommand

from ratings.models import Company, CountryRisk, CreditRating, Profitability, DebtCoverage, Leverage, Liquidity, Size, \
    IndustryRisk, Competitiveness, Rating

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


def create_profitability(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> Profitability:
    profitability = Profitability(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    profitability.save()
    return profitability


def create_debt_coverage(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> DebtCoverage:
    debt_coverage = DebtCoverage(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    debt_coverage.save()
    return debt_coverage


def create_leverage(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> Leverage:
    leverage = Leverage(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    leverage.save()
    return leverage


def create_liquidity(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> Liquidity:
    liquidity = Liquidity(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    liquidity.save()
    return liquidity


def create_size(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> Size:
    size = Size(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    size.save()
    return size


def create_country_risk(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> CountryRisk:
    country_risk = CountryRisk(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    country_risk.save()
    return country_risk


def create_industry_risk(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> IndustryRisk:
    industry_risk = IndustryRisk(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    industry_risk.save()
    return industry_risk


def create_competitiveness(
        latest: float = 1, maximum: float = 1, minimum: float = 1, average: float = 1,
) -> Competitiveness:
    competitiveness = Competitiveness(
        latest=latest,
        maximum=maximum,
        minimum=minimum,
        average=average,
    )
    competitiveness.save()
    return competitiveness


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
                profitability=create_profitability(latest=5.7, maximum=7.7, minimum=5.7, average=6.7),
                debt_coverage=create_debt_coverage(latest=76.2, maximum=81.2, minimum=70.4, average=75.8),
                leverage=create_leverage(latest=40.5, maximum=41.5, minimum=37.7, average=39.6),
                liquidity=create_liquidity(latest=1.11, maximum=1.58, minimum=1.06, average=1.32),
                size=create_size(latest=48_294_200, maximum=48_294_200, minimum=39_320_000, average=43_807_100),
                country_risk=create_country_risk(latest=1, maximum=1, minimum=1, average=1),
                industry_risk=create_industry_risk(latest=1, maximum=1, minimum=1, average=1),
                competitiveness=create_competitiveness(latest=1, maximum=1, minimum=1, average=1),
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
                    for year in range(from_year, to_year + 1):
                        self.create_rating(
                            company=company,
                            credit_rating=create_credit_rating(
                                date=datetime(year=year, month=1, day=1, tzinfo=timezone.utc),
                            ),
                            profitability=create_profitability(),
                            debt_coverage=create_debt_coverage(),
                            leverage=create_leverage(),
                            liquidity=create_liquidity(),
                            size=create_size(),
                            country_risk=create_country_risk(),
                            industry_risk=create_industry_risk(),
                            competitiveness=create_competitiveness(),
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
            profitability: Profitability,
            debt_coverage: DebtCoverage,
            leverage: Leverage,
            liquidity: Liquidity,
            size: Size,
            country_risk: CountryRisk,
            industry_risk: IndustryRisk,
            competitiveness: Competitiveness,
    ) -> Rating:
        rating = Rating(
            company_id=company.id,
            credit_rating=credit_rating,
            profitability=profitability,
            debt_coverage=debt_coverage,
            leverage=leverage,
            liquidity=liquidity,
            size=size,
            country_risk=country_risk,
            industry_risk=industry_risk,
            competitiveness=competitiveness,
        )
        rating.save()
        self.stdout.write(f'        + Rating \'{rating.id}\' ({rating.credit_rating.date}) created')
        return rating
