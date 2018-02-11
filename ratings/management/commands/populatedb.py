from django.core.management.base import BaseCommand, CommandError

from ratings.models import Company
from ratings.models import Rating
from datetime import datetime
from random import choice


class Command(BaseCommand):
    def handle(self, *args, **options):
        companies = [
            Company.objects.get_or_create(name='AAA'),
            Company.objects.get_or_create(name='ABC'),
            Company.objects.get_or_create(name='BBB'),
            Company.objects.get_or_create(name='BCD'),
            Company.objects.get_or_create(name='CCC'),
            Company.objects.get_or_create(name='CDE'),
            Company.objects.get_or_create(name='DDD'),
            Company.objects.get_or_create(name='DEF'),
        ]

        ratings = []
        for i in range(len(companies)):
            company = companies[i][0]
            for j in range(2000, 2018):
                rating = Rating.objects.get_or_create(
                    defaults={
                        'credit_rating': choice(['A', 'B', 'C']),
                        'company_name': company.name
                    },
                    credit_rating_date=datetime(year=j, month=1, day=1),
                    company_id=company.id
                )[0]
