import graphene
from django_filters import FilterSet
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

import credit_report
from credit_report.models import CreditReport, FinancialReport


# Annex G - Credit Report Service
# GraphQL data model
class CreditReportFilter(FilterSet):
    class Meta:
        model = CreditReport
        fields = ['company_id', 'financial_reports__report_date', ]


class CreditReportNode(DjangoObjectType):
    class Meta:
        model = CreditReport
        interfaces = (Node,)


class FinancialReportNode(DjangoObjectType):
    class Meta:
        model = FinancialReport
        interfaces = (Node,)


class Financials(DjangoObjectType):
    class Meta:
        model = credit_report.models.Financials


class CreditReportQuery(graphene.ObjectType):
    credit_reports = DjangoFilterConnectionField(CreditReportNode, filterset_class=CreditReportFilter)
