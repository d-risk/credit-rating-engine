import enum
import uuid

from django.db import models
from django.utils.timezone import now


# Create your models here.
class CreditReport(models.Model):
    company_id = models.UUIDField()
    credit_report_score = models.IntegerField()
    credit_report_rating = models.CharField(max_length=5, )
    credit_report_date = models.DateTimeField(default=now, )


class FinancialsReport(models.Model):
    company_id = models.UUIDField()
    credit_reports = models.ManyToManyField(CreditReport, related_name='financials_reports', )
    financials_report_date = models.DateTimeField(default=now, )


@enum.unique
class Unit(enum.Enum):
    UNKNOWN = enum.auto()
    PERCENTAGE = enum.auto()
    MULTIPLICATIVE = enum.auto()
    CURRENCY = enum.auto()

    @classmethod
    def choices(cls):
        return tuple((x, x) for x in cls)


class FinancialsNumber(models.Model):
    financials_report = models.ForeignKey(FinancialsReport, on_delete=models.PROTECT, related_name='financials_numbers', )
    name = models.CharField(max_length=50, )
    unit = models.CharField(choices=Unit.choices(), default=Unit.CURRENCY, max_length=20, )
    value = models.DecimalField(decimal_places=9, max_digits=99, )


class RiskDriver(models.Model):
    financials_report = models.ForeignKey(FinancialsReport, on_delete=models.PROTECT, related_name='risk_drivers', )
    category = models.CharField(max_length=50, )
    unit = models.CharField(choices=Unit.choices(), default=Unit.UNKNOWN, max_length=20, )


class RiskDriverNumber(models.Model):
    risk_driver = models.ForeignKey(RiskDriver, on_delete=models.PROTECT, related_name='numbers', )
    name = models.CharField(max_length=50, )
    value = models.DecimalField(decimal_places=9, max_digits=99, )


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = models.TextField(unique=True, )
    industry = models.TextField()
    description = models.TextField()
