from datetime import datetime, timezone
from random import randint

from common.management.commands._company import create_company
from common.management.commands._creditreport import create_credit_report, create_financial_report, create_financials
from common.management.commands._randomize import REVENUE, EBIT, EBITDA, INTEREST_EXPENSE, PROFIT_BEFORE_TAX, \
    PROFIT_AFTER_TAX, CASH_EQUIVALENTS, TOTAL_ASSETS, TOTAL_LIABILITIES, TOTAL_DEBT, TOTAL_EQUITY, CURRENT_ASSETS, \
    CURRENT_LIABILITIES
from company.models import Company


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
            financial_report_2014(company),
            financial_report_2015(company),
            financial_report_2016(company),
            financial_report_2017(company),
        ]

        # singtel has one credit report
        create_credit_report(
            company=company,
            credit_score=randint(1, 1000),
            credit_rating='AA',
            report_date=datetime.now(timezone.utc),
            financial_reports=financial_reports,
        )


def financial_report_2014(company):
    # financial report 1
    financial_report = create_financial_report(
        company=company,
        report_date=datetime(year=2014, month=3, day=31, tzinfo=timezone.utc),
    )
    create_financials(financial_report, REVENUE, 16_850_116)
    create_financials(financial_report, EBIT, 3_030_400)
    create_financials(financial_report, EBITDA, 5_166_200)
    create_financials(financial_report, INTEREST_EXPENSE, -301_300)
    create_financials(financial_report, PROFIT_BEFORE_TAX, 4_347_900)
    create_financials(financial_report, PROFIT_AFTER_TAX, 3_652_000)
    create_financials(financial_report, CASH_EQUIVALENTS, 622_500)
    create_financials(financial_report, TOTAL_ASSETS, 39_320_000)
    create_financials(financial_report, TOTAL_LIABILITIES, 15_427_400)
    create_financials(financial_report, TOTAL_DEBT, 15_087_000)
    create_financials(financial_report, TOTAL_EQUITY, 23_868_200)
    create_financials(financial_report, CURRENT_ASSETS, 4_351_300)
    create_financials(financial_report, CURRENT_LIABILITIES, 5_690_000)
    return financial_report


def financial_report_2015(company):
    # financial report 2
    financial_report = create_financial_report(
        company=company,
        report_date=datetime(year=2015, month=3, day=31, tzinfo=timezone.utc),
    )
    create_financials(financial_report, REVENUE, 17_222_900)
    create_financials(financial_report, EBIT, 2_927_200)
    create_financials(financial_report, EBITDA, 5_091_700)
    create_financials(financial_report, INTEREST_EXPENSE, -305_000)
    create_financials(financial_report, PROFIT_BEFORE_TAX, 4_463_000)
    create_financials(financial_report, PROFIT_AFTER_TAX, 3_781_500)
    create_financials(financial_report, CASH_EQUIVALENTS, 562_800)
    create_financials(financial_report, TOTAL_ASSETS, 42_066_800)
    create_financials(financial_report, TOTAL_LIABILITIES, 17_298_900)
    create_financials(financial_report, TOTAL_DEBT, 17_602_500)
    create_financials(financial_report, TOTAL_EQUITY, 24_733_300)
    create_financials(financial_report, CURRENT_ASSETS, 4_767_600)
    create_financials(financial_report, CURRENT_LIABILITIES, 5_756_800)
    return financial_report


def financial_report_2016(company):
    # financial report 3
    financial_report = create_financial_report(
        company=company,
        report_date=datetime(year=2016, month=3, day=31, tzinfo=timezone.utc),
    )
    create_financials(financial_report, REVENUE, 16_961_200)
    create_financials(financial_report, EBIT, 2_864_200)
    create_financials(financial_report, EBITDA, 5_016_100)
    create_financials(financial_report, INTEREST_EXPENSE, -355_400)
    create_financials(financial_report, PROFIT_BEFORE_TAX, 4_580_800)
    create_financials(financial_report, PROFIT_AFTER_TAX, 3_870_800)
    create_financials(financial_report, CASH_EQUIVALENTS, 461_800)
    create_financials(financial_report, TOTAL_ASSETS, 43_565_700)
    create_financials(financial_report, TOTAL_LIABILITIES, 18_563_200)
    create_financials(financial_report, TOTAL_DEBT, 19_005_800)
    create_financials(financial_report, TOTAL_EQUITY, 24_966_800)
    create_financials(financial_report, CURRENT_ASSETS, 5_165_400)
    create_financials(financial_report, CURRENT_LIABILITIES, 6_539_900)
    return financial_report


def financial_report_2017(company: Company):
    # financial report 4
    financial_report = create_financial_report(
        company=company,
        report_date=datetime(year=2017, month=3, day=31, tzinfo=timezone.utc),
    )
    create_financials(financial_report, REVENUE, 16_711_400)
    create_financials(financial_report, EBIT, 2_761_600)
    create_financials(financial_report, EBITDA, 5_003_600)
    create_financials(financial_report, INTEREST_EXPENSE, -370_100)
    create_financials(financial_report, PROFIT_BEFORE_TAX, 4_515_400)
    create_financials(financial_report, PROFIT_AFTER_TAX, 3_852_700)
    create_financials(financial_report, CASH_EQUIVALENTS, 533_800)
    create_financials(financial_report, TOTAL_ASSETS, 48_294_200)
    create_financials(financial_report, TOTAL_LIABILITIES, 20_080_600)
    create_financials(financial_report, TOTAL_DEBT, 19_069_400)
    create_financials(financial_report, TOTAL_EQUITY, 28_191_200)
    create_financials(financial_report, CURRENT_ASSETS, 5_917_500)
    create_financials(financial_report, CURRENT_LIABILITIES, 9_272_300)
    return financial_report
