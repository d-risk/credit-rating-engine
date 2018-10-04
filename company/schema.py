import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

import company.models


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = company.models.Company
        fields = {
            'name': ['iexact', 'icontains', 'istartswith'],
            'industry': ['iexact', 'icontains', 'istartswith'],
        }


class CompanyNode(DjangoObjectType):
    class Meta:
        model = company.models.Company
        interfaces = (graphene.relay.Node,)


class CompanyQuery(graphene.ObjectType):
    company = graphene.relay.Node.Field(CompanyNode)
    companies = DjangoFilterConnectionField(CompanyNode, filterset_class=CompanyFilter)
