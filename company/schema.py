from django_filters import FilterSet
from graphene.relay import Node
from graphene.types import ObjectType, UUID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from company.models import Company


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilter(FilterSet):
    class Meta:
        model = Company
        fields = {
            'name': ['icontains', ],
            'industry': ['icontains', ],
        }


class CompanyNode(DjangoObjectType):
    company_id = UUID(description="The UUID of the company.")

    class Meta:
        model = Company
        interfaces = [Node, ]

    def resolve_company_id(self, info, **args) -> UUID:
        return self.id


class CompanyQuery(ObjectType):
    company = Node.Field(CompanyNode, )
    companies = DjangoFilterConnectionField(CompanyNode, filterset_class=CompanyFilter)
