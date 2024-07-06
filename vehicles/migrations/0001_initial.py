# Generated by Django 4.1.13 on 2024-05-09 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0005_alter_transaction_options_fleet_date_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=250)),
                ('model_description', models.CharField(max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_vehicles', to=settings.AUTH_USER_MODEL)),
                ('fleet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fleet_vehicles', to='transactions.fleet')),
            ],
        ),
    ]
