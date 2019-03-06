# Generated by Django 2.1.7 on 2019-03-06 06:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=50)),
                ('value', models.DecimalField(decimal_places=9, editable=False, max_digits=99)),
            ],
            options={
                'db_table': 'app_financial_data',
            },
        ),
        migrations.CreateModel(
            name='FinancialRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=50)),
                ('value', models.DecimalField(decimal_places=9, editable=False, max_digits=99)),
                ('formula', models.TextField(editable=False)),
            ],
            options={
                'db_table': 'app_financial_ratios',
            },
        ),
        migrations.CreateModel(
            name='FinancialReport',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_id', models.UUIDField(db_index=True, editable=False)),
                ('date_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('currency', models.CharField(editable=False, max_length=5)),
            ],
            options={
                'db_table': 'app_financial_reports',
                'ordering': ['-date_time'],
            },
        ),
        migrations.AddField(
            model_name='financialratio',
            name='financial_report',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='financial_ratios', to='financial_report.FinancialReport'),
        ),
        migrations.AddField(
            model_name='financialdata',
            name='financial_report',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='financial_data', to='financial_report.FinancialReport'),
        ),
    ]
