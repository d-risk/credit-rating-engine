import graphene
from graphene_django import DjangoObjectType

import credit_report.models


class CreditReport(DjangoObjectType):
    class Meta:
        model = credit_report.models.CreditReport


class FinancialsReport(DjangoObjectType):
    class Meta:
        model = credit_report.models.FinancialsReport


Unit = graphene.Enum.from_enum(enum=credit_report.models.Unit, )


class FinancialsNumber(DjangoObjectType):
    class Meta:
        model = credit_report.models.FinancialsNumber


class RiskDriver(DjangoObjectType):
    class Meta:
        model = credit_report.models.RiskDriver


class RiskDriverNumber(DjangoObjectType):
    class Meta:
        model = credit_report.models.RiskDriverNumber


class Company(DjangoObjectType):
    class Meta:
        model = credit_report.models.Company


class Query(graphene.ObjectType):
    company = graphene.Field(Company, id=graphene.UUID())
    companies = graphene.List(Company, company_name=graphene.String())
    credit_reports = graphene.List(CreditReport, company_id=graphene.UUID())

    def resolve_company(self, info, id):
        return credit_report.models.Company.objects.get(id=id)

    def resolve_companies(self, info, company_name):
        return credit_report.models.Company.objects.filter(name__icontains=company_name)

    def resolve_credit_reports(self, info, company_id):
        return credit_report.models.CreditReport.objects.filter(company_id=company_id)
