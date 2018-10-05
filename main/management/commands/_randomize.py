import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from random import randint, choice, random, uniform, randrange
from typing import Tuple, List, Any

from company.models import Company
from credit_report.models import FinancialReport, Unit
from main.management.commands._company import create_company
from main.management.commands._creditreport import create_financial_report, create_credit_report, create_financials, \
    create_risk_driver

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
RATINGS = ['A', 'B', 'C']
NOUN_LIST_URL = 'http://www.desiquintans.com/downloads/nounlist/nounlist.txt'
NOUN_LIST_FILENAME = 'noun_list.txt'


def random_companies(number_of_companies: int, from_year: int, to_year: int):
    companies = []
    path = Path(NOUN_LIST_FILENAME)

    nouns: List[Any] = []
    if path.is_file():
        print(f'Using file {path}')
        with path.open('r') as file:
            nouns = file.read().splitlines()
    else:
        print(f'Downloading noun list from {NOUN_LIST_URL} and saving to file {path}')
        with urllib.request.urlopen(NOUN_LIST_URL) as response, path.open('x') as file:
            decode = response.read().decode()
            file.write(decode)
            nouns = decode.splitlines()

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
    financials_reports: List[FinancialReport] = []
    for year in range(from_year, to_year + 1):
        report_date = datetime(year=year, month=1, day=1, tzinfo=timezone.utc)

        financials_report = create_financial_report(company=company, financial_report_date=report_date, )

        random_financials(financials_report=financials_report)
        random_risk_drivers(financial_report=financials_report)

        financials_reports.append(financials_report)

        create_credit_report(company=company, credit_report_score=randint(1, 1000),
                             credit_report_rating=choice(RATINGS), credit_report_date=report_date,
                             financial_reports=financials_reports, )


def random_financials(financials_report: FinancialReport):
    for name, unit in FINANCIALS:
        create_financials(financial_report=financials_report, name=name, unit=unit, value=random_value(unit))


def random_risk_drivers(financial_report: FinancialReport):
    for name, unit in RISK_DRIVERS:
        create_risk_driver(financial_report=financial_report, name=name, unit=unit, value=random_value(unit), )


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
