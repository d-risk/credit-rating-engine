from django.db.models import Model, UUIDField, CharField, DateTimeField, DecimalField, ManyToManyField, \
    ForeignKey, PROTECT
from django.utils.timezone import now


# Create your models here.
# Annex G - Credit Report Service
# SQL data model
class CreditReport(Model):
    company_id = UUIDField(db_index=True, )
    credit_score = DecimalField(decimal_places=2, max_digits=9, )
    credit_rating = CharField(max_length=5, )
    report_date = DateTimeField(default=now, )

    class Meta:
        db_table = 'app_credit_reports'


class FinancialReport(Model):
    company_id = UUIDField(db_index=True)
    credit_reports = ManyToManyField(CreditReport, related_name='financial_reports', )
    report_date = DateTimeField(default=now, )
    currency = CharField(max_length=5, )

    class Meta:
        db_table = 'app_financial_reports'


class Financials(Model):
    financials_report = ForeignKey(FinancialReport, on_delete=PROTECT, related_name='financials', )
    name = CharField(max_length=50, )
    value = DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_financials'
