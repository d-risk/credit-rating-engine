import graphene
from graphene_django import DjangoObjectType

import credit_report.models


class CreditRating(DjangoObjectType):
    class Meta:
        model = credit_report.models.CreditRating


class Report(DjangoObjectType):
    class Meta:
        model = credit_report.models.Report


Unit = graphene.Enum.from_enum(
    enum=credit_report.models.Unit,
    description='description',
)


class RiskDriver(DjangoObjectType):
    class Meta:
        model = credit_report.models.RiskDriver


class Company(DjangoObjectType):
    class Meta:
        model = credit_report.models.Company


class Query(graphene.ObjectType):
    company = graphene.Field(Company, id=graphene.UUID())
    companies = graphene.List(Company, company_name=graphene.String())
    reports = graphene.List(Report, company_id=graphene.UUID())

    def resolve_company(self, info, id):
        return credit_report.models.Company.objects.get(id=id)

    def resolve_companies(self, info, company_name):
        return credit_report.models.Company.objects.filter(name__icontains=company_name)

    def resolve_reports(self, info, company_id):
        return credit_report.models.Report.objects.filter(company_id=company_id).order_by('-credit_rating__date')
