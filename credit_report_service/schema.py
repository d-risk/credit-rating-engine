from graphene import Schema, ObjectType

from company.schema import CompanyQuery
from credit_report.schema import CreditReportQuery


class Query(CompanyQuery, CreditReportQuery, ObjectType):
    pass


schema: Schema = Schema(query=Query)
