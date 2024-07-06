# Generated by Django 4.1.13 on 2024-05-09 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_date_transaction_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.TimeField(default=datetime.time),
        ),
    ]