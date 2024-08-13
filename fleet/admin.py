from django.contrib import admin
from .models import Fleet
from .forms import CreateFleetForm


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    add_form = CreateFleetForm
    list_display = ['Name', 'date_created', 'owner']
