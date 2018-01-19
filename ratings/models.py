from django.db import models
from django.utils.timezone import now
from datetime import datetime


# Create your models here.
class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class Rating(models.Model):
    RATINGS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    credit_rating = models.CharField(max_length=5, choices=RATINGS)
    credit_rating_date = models.DateTimeField(default=now)
    company_id = models.IntegerField()
    company_name = models.TextField()
