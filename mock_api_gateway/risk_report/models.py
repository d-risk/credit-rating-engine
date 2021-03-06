from django.db import models
from django.utils.timezone import now


# Create your models here.
# SQL data model
class RiskReport(models.Model):
    report_id = models.AutoField(primary_key=True, )
    company_id = models.UUIDField(db_index=True, editable=False, )
    risk_score = models.DecimalField(decimal_places=2, max_digits=9, editable=False, )
    risk_rating = models.CharField(max_length=5, editable=False, )
    date_time = models.DateTimeField(default=now, editable=False, )

    class Meta:
        db_table = 'app_risk_reports'
        ordering = ['-date_time', ]
