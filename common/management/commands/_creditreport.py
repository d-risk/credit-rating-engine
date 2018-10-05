from datetime import datetime
from typing import List

from company.models import Company
from credit_report.models import CreditReport, FinancialReport, Financials


def create_credit_report(
        company: Company,
        credit_score: float,
        credit_rating: str,
        report_date: datetime,
        financial_reports: List[FinancialReport] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        credit_score=credit_score,
        credit_rating=credit_rating,
        report_date=report_date,
    )
    if financial_reports:
        credit_report.financial_reports.set(financial_reports)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.report_date}) created', )
    return credit_report


def create_financial_report(
        company: Company,
        report_date: datetime,
) -> FinancialReport:
    financial_report = FinancialReport.objects.create(
        company_id=company.id,
        report_date=report_date,
        currency='SGD'
    )
    print(
        f'        + Financial Report \'{financial_report.id}\' ({financial_report.report_date}) created', )
    return financial_report


def create_financials(financial_report: FinancialReport, name: str, value: float, ) -> Financials:
    return financial_report.financials.create(name=name, value=value, )
