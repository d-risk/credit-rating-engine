import uuid

from django.db import models
from django.utils.timezone import now


# Create your models here.
class CreditRating(models.Model):
    score = models.IntegerField()
    text = models.CharField(max_length=3)
    date = models.DateTimeField(default=now)


class RiskDriver(models.Model):
    latest = models.DecimalField(max_digits=10, decimal_places=2)
    maximum = models.DecimalField(max_digits=10, decimal_places=2)
    minimum = models.DecimalField(max_digits=10, decimal_places=2)
    average = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class Profitability(RiskDriver):
    pass


class DebtCoverage(RiskDriver):
    pass


class Leverage(RiskDriver):
    pass


class Liquidity(RiskDriver):
    pass


class Size(RiskDriver):
    pass


class CountryRisk(RiskDriver):
    pass


class IndustryRisk(RiskDriver):
    pass


class Competitiveness(RiskDriver):
    pass


class Report(models.Model):
    company_id = models.UUIDField()
    credit_rating = models.ForeignKey(CreditRating, on_delete=models.PROTECT)
    profitability = models.ForeignKey(Profitability, on_delete=models.PROTECT)
    debt_coverage = models.ForeignKey(DebtCoverage, on_delete=models.PROTECT)
    leverage = models.ForeignKey(Leverage, on_delete=models.PROTECT)
    liquidity = models.ForeignKey(Liquidity, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    country_risk = models.ForeignKey(CountryRisk, on_delete=models.PROTECT)
    industry_risk = models.ForeignKey(IndustryRisk, on_delete=models.PROTECT)
    competitiveness = models.ForeignKey(Competitiveness, on_delete=models.PROTECT)


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField(unique=True)
    industry = models.TextField()
    description = models.TextField()
