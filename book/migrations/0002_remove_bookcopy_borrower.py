# Generated by Django 4.2.13 on 2024-06-22 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookcopy',
            name='borrower',
        ),
    ]
