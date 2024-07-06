# Generated by Django 4.1.13 on 2024-05-28 14:17

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_options_fleet_date_created_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='transaction',
            managers=[
                ('transactions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='odo_reading',
            field=models.IntegerField(null=True),
        ),
    ]