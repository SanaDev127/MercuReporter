from django.contrib import admin
from .models import Transaction, Fleet, Merchant, Brand

admin.site.register(Transaction)
admin.site.register(Fleet)
admin.site.register(Merchant)
admin.site.register(Brand)
