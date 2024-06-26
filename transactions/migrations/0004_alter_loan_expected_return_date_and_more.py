# Generated by Django 4.2.13 on 2024-06-26 01:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_loan_expected_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='expected_return_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 11, 1, 29, 14, 285912, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='renovation',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renovations', to='transactions.loan'),
        ),
    ]