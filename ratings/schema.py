import graphene
from graphene_django import DjangoObjectType

import ratings.models


class CreditRating(DjangoObjectType):
    class Meta:
        model = ratings.models.CreditRating


class Profitability(DjangoObjectType):
    class Meta:
        model = ratings.models.Profitability


class DebtCoverage(DjangoObjectType):
    class Meta:
        model = ratings.models.DebtCoverage


class Leverage(DjangoObjectType):
    class Meta:
        model = ratings.models.Leverage


class Liquidity(DjangoObjectType):
    class Meta:
        model = ratings.models.Liquidity


class Size(DjangoObjectType):
    class Meta:
        model = ratings.models.Size


class CountryRisk(DjangoObjectType):
    class Meta:
        model = ratings.models.CountryRisk


class IndustryRisk(DjangoObjectType):
    class Meta:
        model = ratings.models.IndustryRisk


class Competitiveness(DjangoObjectType):
    class Meta:
        model = ratings.models.Competitiveness


class Report(DjangoObjectType):
    class Meta:
        model = ratings.models.Report


class Company(DjangoObjectType):
    class Meta:
        model = ratings.models.Company


class Query(graphene.ObjectType):
    company = graphene.Field(Company, id=graphene.UUID())
    companies = graphene.List(Company, company_name=graphene.String())
    reports = graphene.List(Report, company_id=graphene.UUID())

    def resolve_company(self, info, id):
        return ratings.models.Company.objects.get(id=id)

    def resolve_companies(self, info, company_name):
        return ratings.models.Company.objects.filter(name__icontains=company_name)

    def resolve_reports(self, info, company_id):
        return ratings.models.Report.objects.filter(company_id=company_id).order_by('-credit_rating__date')
