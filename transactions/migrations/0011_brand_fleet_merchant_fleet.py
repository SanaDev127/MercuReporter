# Generated by Django 4.1.13 on 2024-07-16 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0002_remove_fleet_supervisor'),
        ('transactions', '0010_merchant_address_alter_merchant_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='fleet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brands', to='fleet.fleet'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='fleet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fleet_merchants', to='fleet.fleet'),
        ),
    ]
