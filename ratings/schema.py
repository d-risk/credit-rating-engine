import graphene
from graphene_django import DjangoObjectType

from ratings.models import Company, Rating


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company


class RatingType(DjangoObjectType):
    class Meta:
        model = Rating


class Query(graphene.ObjectType):
    companies = graphene.List(CompanyType, text=graphene.String())
    ratings = graphene.List(RatingType, id=graphene.Int())

    def resolve_companies(self, info, text):
        return Company.objects.filter(name__icontains=text)

    def resolve_ratings(self, info, id):
        return Rating.objects.filter(company_id=id).order_by('-credit_rating_date')
