import csv
from datetime import datetime

from credit_report.models import Unit
from main.management.commands._company import create_company
from main.management.commands._creditreport import create_financial_report, create_financials

COLUMN_NAMES: str = [
    'Name of PLC', 'Date', 'Total revenue', 'Cost of revenue', 'Gross profit', 'Research development',
    'Selling general and administrative', 'Non-recurring', 'Others', 'Total operating expenses',
    'Operating income or loss', 'Total other income/expenses net',
    'Earnings before interest and taxes', 'Interest expense', 'Income before tax',
    'Income tax expense', 'Minority interest', 'Net income from continuing ops',
    'Discontinued operations', 'Extraordinary items', 'Effect of accounting changes', 'Other items',
    'Net income', 'Preferred stock and other adjustments', 'Net income applicable to common shares',
    'Cash and cash equivalents', 'Short-term investments', 'Net receivables', 'Inventory',
    'Other current assets', 'Total current assets', 'Long-term investments',
    'Property plant and equipment', 'Goodwill', 'Intangible assets', 'Accumulated amortisation',
    'Other assets', 'Deferred long-term asset charges', 'Total assets', 'Accounts payable',
    'Short/current long-term debt', 'Other current liabilities', 'Total current liabilities',
    'Long-term debt', 'Other liabilities', 'Deferred long-term liability charges', 'Minority interest',
    'Negative goodwill', 'Total liabilities', 'Misc. Stock options warrants',
    'Redeemable preferred stock', 'Preferred stock', 'Common stock', 'Retained earnings',
    'Treasury stock', 'Capital surplus', 'Other stockholder equity', 'Total stockholder equity',
    'Net tangible assets', 'Total Debt', 'Capital', 'Net income', 'Depreciation',
    'Adjustments to net income', 'Changes in accounts receivable', 'Changes in liabilities',
    'Changes in inventory', 'Changes in other operating activities',
    'Total cash flow from operating activities', 'Capital expenditure', 'Investments',
    'Other cash flow from investment activities', 'Total cash flow from investment activities',
    'Dividends paid', 'Sale purchase of stock', 'Net borrowings',
    'Other cash flow from financing activities', 'Total cash flow from financing activities',
    'Effect of exchange rate changes', 'Change in cash and cash equivalents',
]

DATETIME_FORMAT: str = '%Y-%m-%d'


def parse(file_name: str) -> None:
    try:
        with open(file_name) as file:
            reader = csv.DictReader(file)
            if COLUMN_NAMES == reader.fieldnames:
                for row in reader:
                    company_name = row[COLUMN_NAMES[0]]
                    company, created = create_company(company_name)
                    date = datetime.strptime(row[COLUMN_NAMES[1]], DATETIME_FORMAT)
                    financial_report = create_financial_report(company=company, financial_report_date=date)
                    for i in range(2, len(row)):
                        name = COLUMN_NAMES[i]
                        value = float(row[name])
                        create_financials(
                            financial_report=financial_report,
                            name=name,
                            unit=Unit.CURRENCY,
                            value=value,
                        )
            else:
                print(f'Unable read {file_name} because the headers do not match')
    except FileNotFoundError:
        print(f'Cannot find file \'{file_name}\'')
