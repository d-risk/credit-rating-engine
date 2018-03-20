import graphene
import credit_report.schema


class Query(credit_report.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
