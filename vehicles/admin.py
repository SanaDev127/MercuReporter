from django.contrib import admin
from fleet.forms import OwnerAddVehicleForm
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    add_form = OwnerAddVehicleForm
    list_display = ['registration_number', 'model_description', 'fleet', 'date_added', 'addedBy']
    list_filter = ['fleet', 'model_description']
    search_fields = ['registration_number']

