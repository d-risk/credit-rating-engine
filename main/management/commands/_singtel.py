from datetime import datetime, timezone
from random import randint

from company.models import Company
from credit_report.models import FinancialReport, Unit
from main.management.commands._company import create_company
from main.management.commands._creditreport import create_credit_report, create_financial_report, create_financials, \
    create_risk_driver
from main.management.commands._randomize import REVENUE, EBIT, EBITDA, INTEREST_EXPENSE, PROFIT_BEFORE_TAX, \
    PROFIT_AFTER_TAX, CASH_EQUIVALENTS, TOTAL_ASSETS, TOTAL_LIABILITIES, TOTAL_DEBT, TOTAL_EQUITY, CURRENT_ASSETS, \
    CURRENT_LIABILITIES, PROFITABILITY, DEBT_COVERAGE, LEVERAGE, LIQUIDITY, SIZE, COUNTRY_RISK, INDUSTRY_RISK, \
    COMPETITIVENESS, random_risk_drivers


def create_singtel_company():
    company, created = create_company(
        name='Singapore Telecommunications Limited',
        description='Singapore Telecommunications Limited provides integrated infocomm technology solutions to '
                    'enterprise customers primarily in Singapore, Australia, the United States of America, '
                    'and Europe. The company operates through Group Consumer, Group Enterprise, and Group Digital '
                    'Life segments. The Group Consumer segment is involved in carriage business, including mobile, '
                    'pay TV, fixed broadband, and voice, as well as equipment sales. The Group Enterprise segment '
                    'offers mobile, equipment sales, fixed voice and data, managed services, cloud computing, '
                    'cyber security, and IT and professional consulting services. The Group Digital Life segment '
                    'engages in digital marketing, regional video, and advanced analytics and intelligence '
                    'businesses. The company also operates a venture capital fund that focuses its investments on '
                    'technologies and solutions. Singapore Telecommunications Limited is headquartered in Singapore.',
        industry='Telecommunications',
    )
    if created:
        # singtel has 4 financial reports
        financial_reports = [
            financial_report_1(company),
            financial_report_2(company),
            financial_report_3(company),
            financial_report_4(company),
        ]

        # singtel has one credit report
        create_credit_report(
            company=company,
            credit_report_score=randint(1, 1000),
            credit_report_rating='A1',
            credit_report_date=datetime.now(timezone.utc),
            financial_reports=financial_reports,
        )


def financial_report_1(company):
    # financial report 1
    financial_report = create_financial_report(
        company=company,
        financial_report_date=datetime(year=2014, month=3, day=31, tzinfo=timezone.utc),
    )
    financial_report_1_financials(financial_report)
    random_risk_drivers(financial_report=financial_report)
    return financial_report


def financial_report_1_financials(financial_report: FinancialReport):
    create_financials(financial_report, REVENUE, Unit.CURRENCY, 16_850_116)
    create_financials(financial_report, EBIT, Unit.CURRENCY, 3_030_400)
    create_financials(financial_report, EBITDA, Unit.CURRENCY, 5_166_200)
    create_financials(financial_report, INTEREST_EXPENSE, Unit.CURRENCY, -301_300)
    create_financials(financial_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_347_900)
    create_financials(financial_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_652_000)
    create_financials(financial_report, CASH_EQUIVALENTS, Unit.CURRENCY, 622_500)
    create_financials(financial_report, TOTAL_ASSETS, Unit.CURRENCY, 39_320_000)
    create_financials(financial_report, TOTAL_LIABILITIES, Unit.CURRENCY, 15_427_400)
    create_financials(financial_report, TOTAL_DEBT, Unit.CURRENCY, 15_087_000)
    create_financials(financial_report, TOTAL_EQUITY, Unit.CURRENCY, 23_868_200)
    create_financials(financial_report, CURRENT_ASSETS, Unit.CURRENCY, 4_351_300)
    create_financials(financial_report, CURRENT_LIABILITIES, Unit.CURRENCY, 5_690_000)


def financial_report_2(company):
    # financial report 2
    financial_report = create_financial_report(
        company=company,
        financial_report_date=datetime(year=2015, month=3, day=31, tzinfo=timezone.utc),
    )
    financial_report_2_financials(financial_report)
    random_risk_drivers(financial_report=financial_report)
    return financial_report


def financial_report_2_financials(financial_report: FinancialReport):
    create_financials(financial_report, REVENUE, Unit.CURRENCY, 17_222_900)
    create_financials(financial_report, EBIT, Unit.CURRENCY, 2_927_200)
    create_financials(financial_report, EBITDA, Unit.CURRENCY, 5_091_700)
    create_financials(financial_report, INTEREST_EXPENSE, Unit.CURRENCY, -305_000)
    create_financials(financial_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_463_000)
    create_financials(financial_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_781_500)
    create_financials(financial_report, CASH_EQUIVALENTS, Unit.CURRENCY, 562_800)
    create_financials(financial_report, TOTAL_ASSETS, Unit.CURRENCY, 42_066_800)
    create_financials(financial_report, TOTAL_LIABILITIES, Unit.CURRENCY, 17_298_900)
    create_financials(financial_report, TOTAL_DEBT, Unit.CURRENCY, 17_602_500)
    create_financials(financial_report, TOTAL_EQUITY, Unit.CURRENCY, 24_733_300)
    create_financials(financial_report, CURRENT_ASSETS, Unit.CURRENCY, 4_767_600)
    create_financials(financial_report, CURRENT_LIABILITIES, Unit.CURRENCY, 5_756_800)


def financial_report_3(company):
    # financial report 3
    financial_report = create_financial_report(
        company=company,
        financial_report_date=datetime(year=2016, month=3, day=31, tzinfo=timezone.utc),
    )
    financial_report_3_financials(financial_report)
    random_risk_drivers(financial_report=financial_report)

    return financial_report


def financial_report_3_financials(financial_report: FinancialReport):
    create_financials(financial_report, REVENUE, Unit.CURRENCY, 16_961_200)
    create_financials(financial_report, EBIT, Unit.CURRENCY, 2_864_200)
    create_financials(financial_report, EBITDA, Unit.CURRENCY, 5_016_100)
    create_financials(financial_report, INTEREST_EXPENSE, Unit.CURRENCY, -355_400)
    create_financials(financial_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_580_800)
    create_financials(financial_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_870_800)
    create_financials(financial_report, CASH_EQUIVALENTS, Unit.CURRENCY, 461_800)
    create_financials(financial_report, TOTAL_ASSETS, Unit.CURRENCY, 43_565_700)
    create_financials(financial_report, TOTAL_LIABILITIES, Unit.CURRENCY, 18_563_200)
    create_financials(financial_report, TOTAL_DEBT, Unit.CURRENCY, 19_005_800)
    create_financials(financial_report, TOTAL_EQUITY, Unit.CURRENCY, 24_966_800)
    create_financials(financial_report, CURRENT_ASSETS, Unit.CURRENCY, 5_165_400)
    create_financials(financial_report, CURRENT_LIABILITIES, Unit.CURRENCY, 6_539_900)


def financial_report_4(company: Company):
    # financial report 4
    financial_report = create_financial_report(
        company=company,
        financial_report_date=datetime(year=2017, month=3, day=31, tzinfo=timezone.utc),
    )
    financial_report_4_financials(financial_report)
    financial_report_4_risk_drivers(financial_report)

    return financial_report


def financial_report_4_financials(financial_report: FinancialReport):
    create_financials(financial_report, REVENUE, Unit.CURRENCY, 16_711_400)
    create_financials(financial_report, EBIT, Unit.CURRENCY, 2_761_600)
    create_financials(financial_report, EBITDA, Unit.CURRENCY, 5_003_600)
    create_financials(financial_report, INTEREST_EXPENSE, Unit.CURRENCY, -370_100)
    create_financials(financial_report, PROFIT_BEFORE_TAX, Unit.CURRENCY, 4_515_400)
    create_financials(financial_report, PROFIT_AFTER_TAX, Unit.CURRENCY, 3_852_700)
    create_financials(financial_report, CASH_EQUIVALENTS, Unit.CURRENCY, 533_800)
    create_financials(financial_report, TOTAL_ASSETS, Unit.CURRENCY, 48_294_200)
    create_financials(financial_report, TOTAL_LIABILITIES, Unit.CURRENCY, 20_080_600)
    create_financials(financial_report, TOTAL_DEBT, Unit.CURRENCY, 19_069_400)
    create_financials(financial_report, TOTAL_EQUITY, Unit.CURRENCY, 28_191_200)
    create_financials(financial_report, CURRENT_ASSETS, Unit.CURRENCY, 5_917_500)
    create_financials(financial_report, CURRENT_LIABILITIES, Unit.CURRENCY, 9_272_300)


def financial_report_4_risk_drivers(financial_report: FinancialReport):
    create_risk_driver(financial_report=financial_report, name=PROFITABILITY, unit=Unit.PERCENTAGE,
                       value=(5.7 / 100.0), )
    create_risk_driver(financial_report=financial_report, name=DEBT_COVERAGE, unit=Unit.MULTIPLICATIVE, value=76.2, )
    create_risk_driver(financial_report=financial_report, name=LEVERAGE, unit=Unit.PERCENTAGE, value=(40.5 / 100.0), )
    create_risk_driver(financial_report=financial_report, name=LIQUIDITY, unit=Unit.PERCENTAGE, value=(1.11 / 100.0), )
    create_risk_driver(financial_report=financial_report, name=SIZE, unit=Unit.CURRENCY, value=48_294_200, )
    create_risk_driver(financial_report=financial_report, name=COUNTRY_RISK, unit=Unit.PERCENTAGE, value=1, )
    create_risk_driver(financial_report=financial_report, name=INDUSTRY_RISK, unit=Unit.PERCENTAGE, value=1, )
    create_risk_driver(financial_report=financial_report, name=COMPETITIVENESS, unit=Unit.PERCENTAGE, value=1, )
