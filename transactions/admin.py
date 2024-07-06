from django.contrib import admin
from .models import Transaction, Fleet, Merchant, Brand

admin.site.register(Transaction)
admin.site.register(Fleet)
admin.site.register(Merchant)
admin.site.register(Brand)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'time', 'registration_number', 'driver', 'odo_reading', 'quantity', 'amount']
    list_filter = ['client', 'fleet', 'driver', 'registration_number','date']
    search_fields = ['client', 'registration_number']



