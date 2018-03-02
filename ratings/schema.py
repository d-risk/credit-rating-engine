import graphene
from graphene_django import DjangoObjectType

from ratings.models import Company, Rating, CreditRating, Profitability, DebtCoverage, Leverage, \
    Liquidity, Size, CountryRisk, IndustryRisk, Competitiveness


class CreditRatingType(DjangoObjectType):
    class Meta:
        model = CreditRating


class ProfitabilityType(DjangoObjectType):
    class Meta:
        model = Profitability


class DebtCoverageType(DjangoObjectType):
    class Meta:
        model = DebtCoverage


class LeverageType(DjangoObjectType):
    class Meta:
        model = Leverage


class LiquidityType(DjangoObjectType):
    class Meta:
        model = Liquidity


class SizeType(DjangoObjectType):
    class Meta:
        model = Size


class CountryRiskType(DjangoObjectType):
    class Meta:
        model = CountryRisk


class IndustryRiskType(DjangoObjectType):
    class Meta:
        model = IndustryRisk


class CompetitivenessType(DjangoObjectType):
    class Meta:
        model = Competitiveness


class RatingType(DjangoObjectType):
    class Meta:
        model = Rating


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company


class Query(graphene.ObjectType):
    companies = graphene.List(CompanyType, company_name=graphene.String())
    ratings = graphene.List(RatingType, company_id=graphene.UUID())

    def resolve_companies(self, info, company_name):
        return Company.objects.filter(name__icontains=company_name)

    def resolve_ratings(self, info, company_id):
        return Rating.objects.filter(company_id=company_id).order_by('-credit_rating__date')
