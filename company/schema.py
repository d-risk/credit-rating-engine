import graphene
from graphene_django import DjangoObjectType

import company.models


# Annex F - Company Data Service
# GraphQL data model
class Company(DjangoObjectType):
    class Meta:
        model = company.models.Company


class CompanyQuery(graphene.ObjectType):
    company = graphene.Field(Company, id=graphene.UUID())
    companies = graphene.List(Company, company_name=graphene.String())

    def resolve_company(self, info, id):
        return company.models.Company.objects.get(id=id)

    def resolve_companies(self, info, company_name):
        return company.models.Company.objects.filter(name__icontains=company_name)
