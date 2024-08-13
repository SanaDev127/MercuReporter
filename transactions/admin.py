from django.contrib import admin
from .models import Transaction, Merchant, Brand

# admin.site.register(Transaction)
# admin.site.register(Merchant)
# admin.site.register(Brand)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'time', 'registration_number', 'driver', 'odo_reading', 'quantity', 'amount']
    list_filter = ['client', 'fleet', 'driver', 'registration_number', 'date']
    search_fields = ['client', 'registration_number']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['Name', 'fleet']
    list_filter = ['fleet']
    search_fields = ['Name']


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['Name', 'brand', 'fleet']

