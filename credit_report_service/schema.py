from graphene import Schema, ObjectType

from company.schema import CompanyQuery
from credit_report.schema import CreditReportQuery
from financial_report.schema import FinancialReportQuery
from news.schema import NewsQuery


class Query(CompanyQuery, CreditReportQuery, FinancialReportQuery, NewsQuery, ObjectType):
    pass


schema: Schema = Schema(query=Query)
