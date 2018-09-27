import enum
from typing import Tuple, List

from django.db import models
from django.utils.timezone import now


# Create your models here.



@enum.unique
class Unit(enum.Enum):
    UNKNOWN = enum.auto()
    PERCENTAGE = enum.auto()
    MULTIPLICATIVE = enum.auto()
    CURRENCY = enum.auto()

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return list((x.value, x.name) for x in cls)


# Annex G - Credit Report Service
# SQL data model
class CreditReport(models.Model):
    company_id = models.UUIDField()
    credit_score = models.IntegerField()
    credit_rating = models.CharField(max_length=5, )
    report_date = models.DateTimeField(default=now, )

    class Meta:
        db_table = 'app_credit_reports'


class FinancialReport(models.Model):
    company_id = models.UUIDField()
    credit_reports = models.ManyToManyField(CreditReport, related_name='financial_reports', )
    report_date = models.DateTimeField(default=now, )

    class Meta:
        db_table = 'app_financial_reports'


class Financials(models.Model):
    financials_report = models.ForeignKey(FinancialReport, on_delete=models.PROTECT,
                                          related_name='financials', )
    name = models.CharField(max_length=50, )
    # unit = models.CharField(choices=UnitEEE.choices(), max_length=20, )
    unit = models.CharField(max_length=20, )
    value = models.DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_financials'


class RiskDriver(models.Model):
    financial_report = models.ForeignKey(FinancialReport, on_delete=models.PROTECT, related_name='risk_drivers', )

    name = models.CharField(max_length=50, )
    # unit = models.CharField(choices=UnitEEE.choices(), max_length=20, )
    unit = models.CharField(max_length=20, )
    value = models.DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_risk_drivers'
