import datetime
from django.db import models
from accounts.models import CustomUser
from fleet.models import Fleet


class BrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Brand(models.Model):
    Name = models.CharField(max_length=200)
    fleet = models.ForeignKey(Fleet,
                              related_name='brands',
                              null=True,
                              on_delete=models.SET_NULL)
    brands = BrandManager()

    def __str__(self):
        return self.Name


class MerchantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Merchant(models.Model):
    Name = models.CharField(max_length=200, default='Other/Ander')
    latitude = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    brand = models.ForeignKey(Brand,
                              related_name='merchants',
                              null=True,
                              on_delete=models.SET_NULL, blank=True)
    fleet = models.ForeignKey(Fleet,
                              related_name='fleet_merchants',
                              null=True,
                              on_delete=models.SET_NULL)

    merchants = MerchantManager()

    def __str__(self):
        return self.Name


# Get all transactions from a specific driver
class TransactionDriverManager(models.Manager):
    def get_queryset(self, user):
        return super().get_queryset().filter(driver=user)


class TransactionVehicleManager(models.Manager):
    def get_queryset(self, registration_no):
        return super().get_queryset().filter(registration_number=registration_no)


class TransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Transaction(models.Model):
    client = models.ForeignKey(CustomUser,
                               related_name='client_transactions',
                               on_delete=models.CASCADE)
    time = models.TimeField(default=datetime.time)
    date = models.DateField(default=datetime.date.today)
    registration_number = models.CharField(max_length=10)
    driver = models.ForeignKey(CustomUser,
                               related_name='driver_transactions',
                               null=True,
                               on_delete=models.SET_NULL)
    cycle_end_date = models.DateField
    brand = models.ForeignKey(Brand,
                              related_name='brand_transactions',
                              null=True,
                              on_delete=models.SET_NULL)
    description = models.CharField(max_length=200, null=True)
    merchant = models.ForeignKey(Merchant,
                                 related_name='merchant_transactions',
                                 null=True,
                                 on_delete=models.SET_NULL)
    odo_reading = models.IntegerField(null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    fleet = models.ForeignKey(Fleet,
                              related_name='fleet_transactions',
                              null=True,
                              on_delete=models.CASCADE)
    addedBy = models.ForeignKey(CustomUser,
                                related_name='transactions_added',
                                null=True,
                                on_delete=models.SET_NULL)

    transactions = TransactionManager()
    drivers = TransactionDriverManager()
    vehicles = TransactionVehicleManager()

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['client', 'fleet'])
        ]

    def __str__(self):
        return f"Transaction ID: {self.pk}, Reg no: {self.registration_number},  Date: {self.date}, Time: {self.time}," \
               f" Quantity: {self.quantity}L, Amount: R{self.amount}."



