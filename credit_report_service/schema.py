import graphene

import company.schema
import credit_report.schema


class Query(company.schema.CompanyQuery, credit_report.schema.CreditReportQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
