import uuid

from django.db.models import Model, UUIDField, TextField


# Annex F - Company Data Service
# SQL data model
class Company(Model):
    id = UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = TextField(unique=True, db_index=True, )
    industry = TextField(db_index=True, )
    description = TextField()

    class Meta:
        db_table = 'app_companies'
