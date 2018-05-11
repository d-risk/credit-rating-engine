import urllib.request
from datetime import datetime, timezone
from random import choice, uniform, random, randrange, randint
from typing import Tuple, List

from django.core.management.base import BaseCommand

from credit_report.management.commands.parsers import ImportCSV
from credit_report.models import Company, CreditReport, RiskDriver, Unit, FinancialsReport, Financials, \
    RiskDriverData

# financials names
REVENUE = 'Revenue'
EBIT = 'EBIT'
EBITDA = 'EBITDA'
INTEREST_EXPENSE = 'Interest Expense'
PROFIT_BEFORE_TAX = 'Profit Before Tax'
PROFIT_AFTER_TAX = 'Profit After Tax'
CASH_EQUIVALENTS = 'Cash and Cash Equivalents'
TOTAL_ASSETS = 'Total Assets'
TOTAL_LIABILITIES = 'Total Liabilities'
TOTAL_DEBT = 'Total Debt'
TOTAL_EQUITY = 'Total Equity'
CURRENT_ASSETS = 'Current Assets'
CURRENT_LIABILITIES = 'Current Liabilities'
# risk drivers
PROFITABILITY = 'Profitability'
DEBT_COVERAGE = 'Debt Coverage'
LEVERAGE = 'Leverage'
LIQUIDITY = 'Liquidity'
SIZE = 'Size'
COUNTRY_RISK = 'Country Risk'
INDUSTRY_RISK = 'Industry Risk'
COMPETITIVENESS = 'Competitiveness'

AMOUNT = 'amount'
RATINGS = ['A', 'B', 'C']
FINANCIALS: List[Tuple[str, Unit]] = [
    (REVENUE, Unit.CURRENCY),
    (EBIT, Unit.CURRENCY),
    (EBITDA, Unit.CURRENCY),
    (INTEREST_EXPENSE, Unit.CURRENCY),
    (PROFIT_BEFORE_TAX, Unit.CURRENCY),
    (PROFIT_AFTER_TAX, Unit.CURRENCY),
    (CASH_EQUIVALENTS, Unit.CURRENCY),
    (TOTAL_ASSETS, Unit.CURRENCY),
    (TOTAL_LIABILITIES, Unit.CURRENCY),
    (TOTAL_DEBT, Unit.CURRENCY),
    (TOTAL_EQUITY, Unit.CURRENCY),
    (CURRENT_ASSETS, Unit.CURRENCY),
    (CURRENT_LIABILITIES, Unit.CURRENCY),
]
RISK_DRIVERS: List[Tuple[str, Unit]] = [
    (PROFITABILITY, Unit.PERCENTAGE),
    (DEBT_COVERAGE, Unit.MULTIPLICATIVE),
    (LEVERAGE, Unit.PERCENTAGE),
    (LIQUIDITY, Unit.PERCENTAGE),
    (SIZE, Unit.CURRENCY),
    (COUNTRY_RISK, Unit.PERCENTAGE),
    (INDUSTRY_RISK, Unit.PERCENTAGE),
    (COMPETITIVENESS, Unit.PERCENTAGE),
]
RISK_DRIVER_DATA: List[str] = [
    'Latest',
    'Maximum',
    'Minimum',
    'Average',
    'Industry Average',
]


def create_company(
        name: str,
        description: str = '',
        industry: str = '',
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
        credit_report_score: int,
        credit_report_rating: str,
        credit_report_date: datetime,
        financials_reports: List[FinancialsReport] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        credit_report_score=credit_report_score,
        credit_report_rating=credit_report_rating,
        credit_report_date=credit_report_date,
    )
    if financials_reports:
        credit_report.financials_reports.set(financials_reports)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.credit_report_date}) created', )
    return credit_report


def create_financials_report(
        company: Company,
        financials_report_date: datetime,
) -> FinancialsReport:
    financials_report = FinancialsReport.objects.create(
        company_id=company.id,
        financials_report_date=financials_report_date,
    )
    print(
        f'        + Financial Report \'{financials_report.id}\' ({financials_report.financials_report_date}) created', )
    return financials_report


def create_financials(financials_report: FinancialsReport, name: str, unit: Unit,
                      value: float, ) -> Financials:
    return financials_report.financials.create(name=name, unit=unit.name, value=value, )


def create_risk_driver(financials_report: FinancialsReport, category: str, unit: Unit, ) -> RiskDriver:
    return financials_report.risk_drivers.create(category=category, unit=unit.name, )


def create_risk_driver_data(risk_driver: RiskDriver, name: str, value: float, ) -> RiskDriverData:
    return risk_driver.data.create(name=name, value=value, )


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
                random_credit_reports(company=company, from_year=from_year, to_year=to_year, )
    print(f'{len(companies)} companies created, {number_of_companies - len(companies)} duplicates')


def random_credit_reports(company: Company, from_year: int, to_year: int):
    financials_reports: List[FinancialsReport] = []
    for year in range(from_year, to_year + 1):
        report_date = datetime(year=year, month=1, day=1, tzinfo=timezone.utc)

        financials_report = create_financials_report(company=company, financials_report_date=report_date, )

        random_financials(financials_report=financials_report)
        random_risk_drivers(financials_report=financials_report)

        financials_reports.append(financials_report)

        create_credit_report(company=company, credit_report_score=randint(1, 1000),
                             credit_report_rating=choice(RATINGS), credit_report_date=report_date,
                             financials_reports=financials_reports, )


def random_financials(financials_report: FinancialsReport):
    for name, unit in FINANCIALS:
        create_financials(financials_report=financials_report, name=name, unit=unit, value=random_value(unit))


def random_risk_drivers(financials_report: FinancialsReport):
    for category, unit in RISK_DRIVERS:
        risk_driver = create_risk_driver(financials_report=financials_report, category=category, unit=unit)
        random_risk_driver_data(risk_driver=risk_driver, unit=unit)


def random_risk_driver_data(risk_driver: RiskDriver, unit: Unit):
    for name in RISK_DRIVER_DATA:
        create_risk_driver_data(risk_driver=risk_driver, name=name, value=random_value(unit))


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


def create_singtel_company():
    company, created = create_company(
        name='Singapore Telecommunications Limited',
        description='Singapore Telecommunications Limited provides integrated infocomm technology solutions to enterprise customers primarily in Singapore, Australia, the United States of America, and Europe. The company operates through Group Consumer, Group Enterprise, and Group Digital Life segments. The Group Consumer segment is involved in carriage business, including mobile, pay TV, fixed broadband, and voice, as well as equipment sales. The Group Enterprise segment offers mobile, equipment sales, fixed voice and data, managed services, cloud computing, cyber security, and IT and professional consulting services. The Group Digital Life segment engages in digital marketing, regional video, and advanced analytics and intelligence businesses. The company also operates a venture capital fund that focuses its investments on technologies and solutions. Singapore Telecommunications Limited is headquartered in Singapore.',
        industry='Telecommunications',
    )
    if created:
        # singtel has 4 financial reports
        financials_reports = [
            financials_report_1(company),
            financials_report_2(company),
            financials_report_3(company),
            financials_report_4(company),
        ]

        # singtel has one credit report
        create_credit_report(
            company=company,
            credit_report_score=randint(1, 1000),
            credit_report_rating='A1',
            credit_report_date=datetime.now(timezone.utc),
            financials_reports=financials_reports,
        )


def financials_report_1(company):
    # financial report 1
    financials_report = create_financials_report(
        company=company,
        financials_report_date=datetime(year=2014, month=3, day=31, tzinfo=timezone.utc),
    )
    financials_report_1_financials(financials_report)
    random_risk_drivers(financials_report=financials_report)
    return financials_report


def financials_report_1_financials(financials_report: FinancialsReport):
    create_financials(financials_report, REVENUE, Unit.CURRENCY, 16_850_116)
    create_financials(financials_report, EBIT, Unit.CURRENCY, 3_030_400)
    create_financials(financials_report, EBITDA, Unit.CURRENCY, 5_166_200)
    create_financials(financials_report, INTEREST_EXPENSE, Unit.CURRENCY, -301_300)
    create_financials(financials_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_347_900)
    create_financials(financials_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_652_000)
    create_financials(financials_report, CASH_EQUIVALENTS, Unit.CURRENCY, 622_500)
    create_financials(financials_report, TOTAL_ASSETS, Unit.CURRENCY, 39_320_000)
    create_financials(financials_report, TOTAL_LIABILITIES, Unit.CURRENCY, 15_427_400)
    create_financials(financials_report, TOTAL_DEBT, Unit.CURRENCY, 15_087_000)
    create_financials(financials_report, TOTAL_EQUITY, Unit.CURRENCY, 23_868_200)
    create_financials(financials_report, CURRENT_ASSETS, Unit.CURRENCY, 4_351_300)
    create_financials(financials_report, CURRENT_LIABILITIES, Unit.CURRENCY, 5_690_000)


def financials_report_2(company):
    # financial report 2
    financials_report = create_financials_report(
        company=company,
        financials_report_date=datetime(year=2015, month=3, day=31, tzinfo=timezone.utc),
    )
    financials_report_2_financials(financials_report)
    random_risk_drivers(financials_report=financials_report)
    return financials_report


def financials_report_2_financials(financials_report: FinancialsReport):
    create_financials(financials_report, REVENUE, Unit.CURRENCY, 17_222_900)
    create_financials(financials_report, EBIT, Unit.CURRENCY, 2_927_200)
    create_financials(financials_report, EBITDA, Unit.CURRENCY, 5_091_700)
    create_financials(financials_report, INTEREST_EXPENSE, Unit.CURRENCY, -305_000)
    create_financials(financials_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_463_000)
    create_financials(financials_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_781_500)
    create_financials(financials_report, CASH_EQUIVALENTS, Unit.CURRENCY, 562_800)
    create_financials(financials_report, TOTAL_ASSETS, Unit.CURRENCY, 42_066_800)
    create_financials(financials_report, TOTAL_LIABILITIES, Unit.CURRENCY, 17_298_900)
    create_financials(financials_report, TOTAL_DEBT, Unit.CURRENCY, 17_602_500)
    create_financials(financials_report, TOTAL_EQUITY, Unit.CURRENCY, 24_733_300)
    create_financials(financials_report, CURRENT_ASSETS, Unit.CURRENCY, 4_767_600)
    create_financials(financials_report, CURRENT_LIABILITIES, Unit.CURRENCY, 5_756_800)


def financials_report_3(company):
    # financial report 3
    financials_report = create_financials_report(
        company=company,
        financials_report_date=datetime(year=2016, month=3, day=31, tzinfo=timezone.utc),
    )
    financials_report_3_financials(financials_report)
    random_risk_drivers(financials_report=financials_report)

    return financials_report


def financials_report_3_financials(financials_report: FinancialsReport):
    create_financials(financials_report, REVENUE, Unit.CURRENCY, 16_961_200)
    create_financials(financials_report, EBIT, Unit.CURRENCY, 2_864_200)
    create_financials(financials_report, EBITDA, Unit.CURRENCY, 5_016_100)
    create_financials(financials_report, INTEREST_EXPENSE, Unit.CURRENCY, -355_400)
    create_financials(financials_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_580_800)
    create_financials(financials_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_870_800)
    create_financials(financials_report, CASH_EQUIVALENTS, Unit.CURRENCY, 461_800)
    create_financials(financials_report, TOTAL_ASSETS, Unit.CURRENCY, 43_565_700)
    create_financials(financials_report, TOTAL_LIABILITIES, Unit.CURRENCY, 18_563_200)
    create_financials(financials_report, TOTAL_DEBT, Unit.CURRENCY, 19_005_800)
    create_financials(financials_report, TOTAL_EQUITY, Unit.CURRENCY, 24_966_800)
    create_financials(financials_report, CURRENT_ASSETS, Unit.CURRENCY, 5_165_400)
    create_financials(financials_report, CURRENT_LIABILITIES, Unit.CURRENCY, 6_539_900)


def financials_report_4(company: Company):
    # financial report 4
    financials_report = create_financials_report(
        company=company,
        financials_report_date=datetime(year=2017, month=3, day=31, tzinfo=timezone.utc),
    )
    financials_report_4_financials(financials_report)
    financials_report_4_risk_drivers(financials_report)

    return financials_report


def financials_report_4_financials(financials_report: FinancialsReport):
    create_financials(financials_report, REVENUE, Unit.CURRENCY, 16_711_400)
    create_financials(financials_report, EBIT, Unit.CURRENCY, 2_761_600)
    create_financials(financials_report, EBITDA, Unit.CURRENCY, 5_003_600)
    create_financials(financials_report, INTEREST_EXPENSE, Unit.CURRENCY, -370_100)
    create_financials(financials_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_515_400)
    create_financials(financials_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_852_700)
    create_financials(financials_report, CASH_EQUIVALENTS, Unit.CURRENCY, 533_800)
    create_financials(financials_report, TOTAL_ASSETS, Unit.CURRENCY, 48_294_200)
    create_financials(financials_report, TOTAL_LIABILITIES, Unit.CURRENCY, 20_080_600)
    create_financials(financials_report, TOTAL_DEBT, Unit.CURRENCY, 19_069_400)
    create_financials(financials_report, TOTAL_EQUITY, Unit.CURRENCY, 28_191_200)
    create_financials(financials_report, CURRENT_ASSETS, Unit.CURRENCY, 5_917_500)
    create_financials(financials_report, CURRENT_LIABILITIES, Unit.CURRENCY, 9_272_300)


def financials_report_4_risk_drivers(financials_report: FinancialsReport):
    risk_driver = create_risk_driver(financials_report=financials_report, category=PROFITABILITY,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=5.7 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=7.7 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=5.7 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=6.7 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=DEBT_COVERAGE,
                                     unit=Unit.MULTIPLICATIVE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=76.2)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=81.2)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=70.4)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=75.8)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=LEVERAGE,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=40.5 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=41.5 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=37.7 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=39.6 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=LIQUIDITY,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=1.11 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=1.58 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=1.06 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=1.32 / 100.0)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=SIZE, unit=Unit.CURRENCY, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=48_294_200)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=48_294_200)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=39_320_000)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=43_807_100)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=COUNTRY_RISK,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=INDUSTRY_RISK,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)
    risk_driver = create_risk_driver(financials_report=financials_report, category=COMPETITIVENESS,
                                     unit=Unit.PERCENTAGE, )
    create_risk_driver_data(risk_driver=risk_driver, name='Latest', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Maximum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Minimum', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Average', value=1)
    create_risk_driver_data(risk_driver=risk_driver, name='Industry Average', value=1)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(AMOUNT, type=int)

    def handle(self, *args, **options):
        ImportCSV.parse('financial-reports.csv')
        # create_singtel_company()
        # random_companies(options[AMOUNT], 2015, 2018)


