import logging
from typing import List

import django_filters
import graphene
import graphene_django
import graphql
from django.db.models import QuerySet, functions
from graphene import relay
from graphene_django import filter

from mock_api_gateway.company.models import Company as CompanyModel
from mock_api_gateway.risk_report.models import RiskReport as RiskReportModel
from mock_api_gateway.risk_report.schema import RiskReport


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilterByName(django_filters.FilterSet):
    name = django_filters.CharFilter(required=True, lookup_expr='istartswith')

    class Meta:
        model = CompanyModel
        fields = ['name', ]

    @property
    def qs(self):
        return super(CompanyFilterByName, self).qs.order_by(functions.Upper('name'))


class Company(graphene_django.DjangoObjectType):
    id = relay.GlobalID(description='A global ID for reactive paging purposes', )
    company_id = graphene.UUID(description='The UUID of the company', )
    name = graphene.String(description='The name of the company', )
    industry = graphene.String(description='The industry in which the company operates', )
    description = graphene.String(description='A description of the company', )
    exchange = graphene.String(description='The stock exchange in which the company is listed', )

    # TODO figure out the proper type for country
    # country = graphene.Enum(description='The country in which the company operates',)

    class Meta:
        model = CompanyModel
        interfaces = (relay.Node,)
        description = 'General information about a company'


class CompanyRating(graphene.ObjectType):
    company = graphene.Field(
        type=Company,
        required=True,
        description='Information about a company',
    )
    risk_report = graphene.Field(
        type=RiskReport,
        required=True,
        description='The latest risk rating associated to the company',
    )

    class Meta:
        interfaces = (relay.Node,)


class CompanyRatingConnection(relay.Connection):
    class Meta:
        node = CompanyRating


class CompanyQuery(graphene.ObjectType):
    company = graphene.Field(
        type=Company,
        description='Retrieve general information about a company using a UUID',
        company_id=graphene.UUID(required=True, description='The UUID of a company', ),
    )
    companies_by_name = filter.DjangoFilterConnectionField(
        type=Company,
        description='Search for companies that contains the given name',
        filterset_class=CompanyFilterByName,
    )
    companies_by_ratings = relay.ConnectionField(
        type=CompanyRatingConnection,
        description='Search for companies that matches the given ratings',
        ratings=graphene.List(of_type=graphene.NonNull(graphene.String), required=True, ),
    )

    def resolve_company(
            self,
            info: graphql.ResolveInfo,
            company_id: graphene.UUID,
            **kwargs,
    ) -> Company:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return CompanyModel.objects.get(company_id=company_id, )

    def resolve_companies_by_ratings(
            self,
            info: graphql.ResolveInfo,
            ratings: graphene.List,
            **kwargs,
    ) -> List[CompanyRating]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        companies: QuerySet = CompanyModel.objects.all()
        risk_reports: QuerySet = RiskReportModel.objects.all()
        results: List[CompanyRating] = []
        for company in companies:
            risk_report: RiskReportModel = risk_reports.filter(
                company_id=company.company_id
            ).latest(field_name='date_time')
            if risk_report.risk_rating in ratings:
                results.append(CompanyRating(company=company, risk_report=risk_report))
        return results
