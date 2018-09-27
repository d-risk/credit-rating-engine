from datetime import datetime
from typing import Tuple, List

from credit_report.models import FinancialReport, CreditReport, Unit, Financials, RiskDriver
from company.models import Company


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
        financial_reports: List[FinancialReport] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        credit_score=credit_report_score,
        credit_rating=credit_report_rating,
        report_date=credit_report_date,
    )
    if financial_reports:
        credit_report.financial_reports.set(financial_reports)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.report_date}) created', )
    return credit_report


def create_financial_report(
        company: Company,
        financial_report_date: datetime,
) -> FinancialReport:
    financial_report = FinancialReport.objects.create(
        company_id=company.id,
        report_date=financial_report_date,
    )
    print(
        f'        + Financial Report \'{financial_report.id}\' ({financial_report.report_date}) created', )
    return financial_report


def create_financials(financial_report: FinancialReport, name: str, unit: Unit,
                      value: float, ) -> Financials:
    return financial_report.financials.create(name=name, unit=unit.name, value=value, )


def create_risk_driver(financial_report: FinancialReport, name: str, unit: Unit, value: float, ) -> RiskDriver:
    return financial_report.risk_drivers.create(name=name, unit=unit.name, value=value, )
