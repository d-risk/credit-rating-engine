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


class FinancialReport(models.Model):
    company_id = models.UUIDField()
    credit_report = models.ManyToManyField(CreditReport, related_name='financial_reports', )
    financial_report_date = models.DateTimeField(default=now, )


@enum.unique
class Unit(enum.Enum):
    UNKNOWN = enum.auto()
    PERCENTAGE = enum.auto()
    MULTIPLICATIVE = enum.auto()
    CURRENCY = enum.auto()

    @classmethod
    def choices(cls):
        return tuple((x, x) for x in cls)


class Financial(models.Model):
    financial_report = models.ForeignKey(FinancialReport, on_delete=models.PROTECT, related_name='financials', )
    name = models.CharField(max_length=50, )
    unit = models.CharField(choices=Unit.choices(), default=Unit.CURRENCY, max_length=20, )
    value = models.DecimalField(decimal_places=9, max_digits=99, )


class RiskDriver(models.Model):
    financial_report = models.ForeignKey(FinancialReport, on_delete=models.PROTECT, related_name='risk_drivers', )
    name = models.CharField(max_length=50, )
    unit = models.CharField(choices=Unit.choices(), default=Unit.UNKNOWN, max_length=20, )
    latest = models.DecimalField(decimal_places=9, max_digits=99, )
    maximum = models.DecimalField(decimal_places=9, max_digits=99, )
    minimum = models.DecimalField(decimal_places=9, max_digits=99, )
    average = models.DecimalField(decimal_places=9, max_digits=99, )
    industry_average = models.DecimalField(decimal_places=9, max_digits=99, )


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = models.TextField(unique=True, )
    industry = models.TextField()
    description = models.TextField()
