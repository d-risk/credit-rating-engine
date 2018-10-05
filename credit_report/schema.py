import graphene
from django_filters import FilterSet, NumberFilter
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
        fields = ['company_id', ]

    @property
    def qs(self: FilterSet):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all().order_by('-report_date')
            if self.is_bound:
                # ensure form validation before filtering
                self.errors
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs


class FinancialReportFilter(FilterSet):
    class Meta:
        model = FinancialReport
        fields = ['report_date', ]

    year = NumberFilter(field_name='report_date', lookup_expr='year')
    from_year = NumberFilter(field_name='report_date', lookup_expr='year__gte')
    to_year = NumberFilter(field_name='report_date', lookup_expr='year__lte')

    @property
    def qs(self: FilterSet):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all().order_by('-report_date')
            if self.is_bound:
                # ensure form validation before filtering
                self.errors
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs


class FinancialReportNode(DjangoObjectType):
    class Meta:
        model = FinancialReport
        interfaces = [Node, ]


class CreditReportNode(DjangoObjectType):
    class Meta:
        model = CreditReport
        interfaces = [Node, ]

    financial_reports = DjangoFilterConnectionField(
        FinancialReportNode,
        order_by='report_date',
        filterset_class=FinancialReportFilter,
    )


class Financials(DjangoObjectType):
    class Meta:
        model = credit_report.models.Financials


class CreditReportQuery(graphene.ObjectType):
    credit_reports = DjangoFilterConnectionField(
        CreditReportNode,
        order_by='-report_dated',
        filterset_class=CreditReportFilter,
    )
