import urllib.request
from datetime import datetime, timezone
from random import choice, uniform, random, randrange, randint
from typing import Tuple, List

from django.core.management.base import BaseCommand

from credit_report.models import Company, CreditReport, RiskDriver, Unit, FinancialReport, Financial

AMOUNT = 'amount'
RATINGS = ['A', 'B', 'C']
FINANCIALS: List[Tuple[str, Unit]] = [
    ('Revenue', Unit.CURRENCY),
    ('EBIT', Unit.CURRENCY),
    ('EBITDA', Unit.CURRENCY),
    ('Interest Expense', Unit.CURRENCY),
    ('Profit Before Tax', Unit.CURRENCY),
    ('Profit After Tax', Unit.CURRENCY),
    ('Cash and Cash Equivalents', Unit.CURRENCY),
    ('Total Assets', Unit.CURRENCY),
    ('Total Liabilities', Unit.CURRENCY),
    ('Total Debt', Unit.CURRENCY),
    ('Total Equity', Unit.CURRENCY),
    ('Current Assets', Unit.CURRENCY),
    ('Current Liabilities', Unit.CURRENCY),
]
RISK_DRIVERS: List[Tuple[str, Unit]] = [
    ('Profitability', Unit.PERCENTAGE),
    ('Debt Coverage', Unit.MULTIPLICATIVE),
    ('Leverage', Unit.PERCENTAGE),
    ('Liquidity', Unit.PERCENTAGE),
    ('Size', Unit.CURRENCY),
    ('Country Risk', Unit.PERCENTAGE),
    ('Industry Risk', Unit.PERCENTAGE),
    ('Competitiveness', Unit.PERCENTAGE),
]


def create_company(
        name: str,
        description: str = 'random industry',
        industry: str = 'random description',
) -> Tuple[Company, bool]:
    company, created = Company.objects.get_or_create(
        defaults={
            'description': description,
            'industry': industry,
        },
        name=name,
    )
    s = 'created' if created else 'already exists'
    print(f'    + Company \'{company.name}\' ({company.id}) {s}')
    return company, created


def create_credit_report(
        company: Company,
        credit_report_score: int = randint(1, 1000),
        credit_report_rating: str = choice(RATINGS),
        credit_report_date: datetime = datetime.now(timezone.utc),
        financial_reports: List[FinancialReport] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        credit_report_score=credit_report_score,
        credit_report_rating=credit_report_rating,
        credit_report_date=credit_report_date,
    )
    credit_report.financial_reports.set(financial_reports)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.credit_report_date}) created', )
    return credit_report


def create_financial_report(
        company: Company,
        financial_report_date: datetime,
        financials: List[Financial] = None,
        risk_drivers: List[RiskDriver] = None,
) -> FinancialReport:
    financial_report = FinancialReport.objects.create(
        company_id=company.id,
        financial_report_date=financial_report_date,
    )
    if financials:
        financial_report.financials.set(financials, bulk=False)
    else:
        financial_report.financials.set(random_financials(), bulk=False)
    if risk_drivers:
        financial_report.risk_drivers.set(risk_drivers, bulk=False)
    else:
        financial_report.risk_drivers.set(random_risk_drivers(), bulk=False)
    print(f'        + Financial Report \'{financial_report.id}\' ({financial_report.financial_report_date}) created', )
    return financial_report


def create_financial(name: str, unit: Unit = Unit.CURRENCY, value: float = None, ) -> Financial:
    return Financial(
        name=name,
        unit=unit,
        value=value if value else random_value(unit),
    )


def create_risk_driver(name: str, unit: Unit = Unit.UNKNOWN,
                       latest: float = None, maximum: float = None, minimum: float = None, average: float = None,
                       industry_average: float = None,
                       ) -> RiskDriver:
    return RiskDriver(
        name=name,
        unit=unit,
        latest=latest if latest else random_value(unit),
        maximum=maximum if maximum else random_value(unit),
        minimum=minimum if minimum else random_value(unit),
        average=average if average else random_value(unit),
        industry_average=industry_average if industry_average else random_value(unit),
    )


def random_companies(number_of_companies: int, from_year: int, to_year: int):
    companies = []
    with urllib.request.urlopen('http://www.desiquintans.com/downloads/nounlist/nounlist.txt') as response:
        nouns = response.read().decode().splitlines()
        print(f'Using {len(nouns)} nouns to create {number_of_companies} companies:')
        for i in range(number_of_companies):
            company, created = create_company(
                name=f'{choice(nouns)} {choice(nouns)} {choice(nouns)}',
            )
            if created:
                companies.append(company)
                random_credit_reports(company=company, from_year=from_year, to_year=to_year)
    print(f'{len(companies)} companies created, {number_of_companies - len(companies)} duplicates')


def random_credit_reports(company: Company, from_year: int, to_year: int):
    financial_reports: List[FinancialReport] = []
    for year in range(from_year, to_year + 1):
        report_date = datetime(year=year, month=1, day=1, tzinfo=timezone.utc)
        financial_reports.append(create_financial_report(
            company=company,
            financial_report_date=report_date,
        ))
        create_credit_report(
            company=company,
            credit_report_date=report_date,
            financial_reports=financial_reports,
        )


def random_financials() -> List[Financial]:
    return [create_financial(name=name, unit=unit) for name, unit in FINANCIALS]


def random_risk_drivers() -> List[RiskDriver]:
    return [create_risk_driver(name=name, unit=unit) for name, unit in RISK_DRIVERS]


def random_value(unit: Unit) -> float:
    value = 1
    if unit is Unit.PERCENTAGE:
        value = random()
    elif unit is Unit.MULTIPLICATIVE:
        value = uniform(0, 1000)
    elif unit is Unit.CURRENCY:
        value = uniform(0, 999_999_999_999)
    elif unit is Unit.UNKNOWN:
        value = randrange(999_999_999_999)
    return value


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(AMOUNT, type=int)

    def handle(self, *args, **options):
        self.create_singtel_company()
        random_companies(options[AMOUNT], 2015, 2018)

    @staticmethod
    def create_singtel_company():
        company, created = create_company(
            name='Singapore Telecommunications Limited',
            description='Singapore Telecommunications Limited provides integrated infocomm technology solutions to enterprise customers primarily in Singapore, Australia, the United States of America, and Europe. The company operates through Group Consumer, Group Enterprise, and Group Digital Life segments. The Group Consumer segment is involved in carriage business, including mobile, pay TV, fixed broadband, and voice, as well as equipment sales. The Group Enterprise segment offers mobile, equipment sales, fixed voice and data, managed services, cloud computing, cyber security, and IT and professional consulting services. The Group Digital Life segment engages in digital marketing, regional video, and advanced analytics and intelligence businesses. The company also operates a venture capital fund that focuses its investments on technologies and solutions. Singapore Telecommunications Limited is headquartered in Singapore.',
            industry='Telecommunications',
        )
        if created:
            # singtel has one credit report
            create_credit_report(
                company=company,
                credit_report_rating='A1',
                #  singtel has 4 financial reports
                financial_reports=[
                    create_financial_report(
                        company=company,
                        financial_report_date=datetime(year=2014, month=3, day=31, tzinfo=timezone.utc),
                        financials=[
                        ],
                        risk_drivers=[
                        ],
                    ),
                    create_financial_report(
                        company=company,
                        financial_report_date=datetime(year=2015, month=3, day=31, tzinfo=timezone.utc),
                        financials=[
                        ],
                        risk_drivers=[
                        ],
                    ),
                    create_financial_report(
                        company=company,
                        financial_report_date=datetime(year=2016, month=3, day=31, tzinfo=timezone.utc),
                        financials=[
                        ],
                        risk_drivers=[
                        ],
                    ),
                    create_financial_report(
                        company=company,
                        financial_report_date=datetime(year=2017, month=3, day=31, tzinfo=timezone.utc),
                        financials=[
                        ],
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
                            create_risk_driver('Size', Unit.CURRENCY, latest=48_294_200, maximum=48_294_200,
                                               minimum=39_320_000,
                                               average=43_807_100),
                            create_risk_driver('Country Risk', Unit.PERCENTAGE, latest=1, maximum=1, minimum=1,
                                               average=1),
                            create_risk_driver('Industry Risk', Unit.PERCENTAGE, latest=1, maximum=1, minimum=1,
                                               average=1),
                            create_risk_driver('Competitiveness', Unit.PERCENTAGE, latest=1, maximum=1, minimum=1,
                                               average=1),
                        ],
                    ),
                ],
            )
