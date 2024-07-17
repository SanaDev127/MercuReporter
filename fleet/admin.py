from django.contrib import admin
from .models import Fleet


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ['Name', 'date_created', 'owner']
