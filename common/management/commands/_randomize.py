import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from random import randint, choice, uniform
from typing import List

from common.management.commands._company import create_company
from common.management.commands._creditreport import create_financial_report, create_credit_report, create_financials
from company.models import Company
from credit_report.models import FinancialReport

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
FINANCIALS: List[str] = [
    REVENUE,
    EBIT,
    EBITDA,
    INTEREST_EXPENSE,
    PROFIT_BEFORE_TAX,
    PROFIT_AFTER_TAX,
    CASH_EQUIVALENTS,
    TOTAL_ASSETS,
    TOTAL_LIABILITIES,
    TOTAL_DEBT,
    TOTAL_EQUITY,
    CURRENT_ASSETS,
    CURRENT_LIABILITIES,
]
RATINGS = ['A', 'B', 'C']
NOUN_LIST_URL = 'http://www.desiquintans.com/downloads/nounlist/nounlist.txt'
NOUN_LIST_FILENAME = 'noun_list.txt'


def random_companies(number_of_companies: int, from_year: int, to_year: int):
    companies = []
    path = Path(NOUN_LIST_FILENAME)

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
        report_date = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc)
        financials_report = create_financial_report(company=company, report_date=report_date, )
        random_financials(financials_report=financials_report)
        financials_reports.append(financials_report)
        create_credit_report(
            company=company,
            credit_score=uniform(1, 99),
            credit_rating=choice(RATINGS),
            report_date=report_date,
            financial_reports=financials_reports,
        )


def random_financials(financials_report: FinancialReport):
    for name in FINANCIALS:
        create_financials(financial_report=financials_report, name=name, value=uniform(0, 999_999_999_999))
