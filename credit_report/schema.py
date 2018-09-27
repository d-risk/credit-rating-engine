import graphene
from graphene_django import DjangoObjectType

import credit_report.models


# Annex G - Credit Report Service
# GraphQL data model
class CreditReport(DjangoObjectType):
    class Meta:
        model = credit_report.models.CreditReport


class FinancialReport(DjangoObjectType):
    class Meta:
        model = credit_report.models.FinancialReport


class Financials(DjangoObjectType):
    class Meta:
        model = credit_report.models.Financials


class RiskDriver(DjangoObjectType):
    class Meta:
        model = credit_report.models.RiskDriver


class CreditReportQuery(graphene.ObjectType):
    credit_reports = graphene.List(CreditReport, company_id=graphene.UUID())

    def resolve_credit_reports(self, info, company_id):
        return credit_report.models.CreditReport.objects.filter(company_id=company_id)
