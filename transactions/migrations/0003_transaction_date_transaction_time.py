# Generated by Django 4.1.13 on 2024-05-09 13:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_merchant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date(2024, 5, 9)),
        ),
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.TimeField(default=datetime.time(13, 46, 13, 829114)),
        ),
    ]
