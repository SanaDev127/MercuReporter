# Generated by Django 4.1.13 on 2024-07-06 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=220)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_fleets', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_fleets', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('fleets', django.db.models.manager.Manager()),
            ],
        ),
    ]
