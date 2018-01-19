import graphene
import ratings.schema


class Query(ratings.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
