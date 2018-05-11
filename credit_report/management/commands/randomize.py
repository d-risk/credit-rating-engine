import urllib.request
from datetime import datetime, timezone
from random import randint, choice, random, uniform, randrange
from typing import List, Tuple

from credit_report.management.commands.models import create_company, create_credit_report, create_financials_report, \
    create_financials, create_risk_driver, create_risk_driver_data
from credit_report.models import Company, FinancialsReport, RiskDriver, Unit

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

RATINGS = ['A', 'B', 'C']


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
