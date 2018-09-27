import uuid

from django.db import models


# Annex F - Company Data Service
# SQL data model
class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = models.TextField(unique=True, )
    industry = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'app_companies'
