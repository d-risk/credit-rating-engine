from datetime import datetime
from typing import Tuple, List

from credit_report.models import Company, FinancialsReport, CreditReport, Unit, Financials, RiskDriver, RiskDriverData


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
