import enum
import uuid

from django.db import models
from django.utils.timezone import now


# Create your models here.
class CreditRating(models.Model):
    score = models.IntegerField()
    text = models.CharField(max_length=3, )
    date = models.DateTimeField(default=now, )


class Report(models.Model):
    company_id = models.UUIDField()
    credit_rating = models.OneToOneField(CreditRating, on_delete=models.PROTECT)


@enum.unique
class Unit(enum.Enum):
    UNKNOWN = enum.auto()
    PERCENTAGE = enum.auto()
    MULTIPLICATIVE = enum.auto()

    @classmethod
    def choices(cls):
        return tuple((x, x) for x in cls)


class RiskDriver(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT, related_name='risk_drivers', )
    name = models.CharField(max_length=20, )
    unit = models.CharField(choices=Unit.choices(), default=Unit.UNKNOWN, max_length=10, )
    latest = models.DecimalField(decimal_places=2, max_digits=99, )
    maximum = models.DecimalField(decimal_places=2, max_digits=99, )
    minimum = models.DecimalField(decimal_places=2, max_digits=99, )
    average = models.DecimalField(decimal_places=2, max_digits=99, )


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField(unique=True)
    industry = models.TextField()
    description = models.TextField()
