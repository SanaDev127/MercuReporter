from django.db import models
from accounts.models import CustomUser


class Fleet(models.Model):
    Name = models.CharField(max_length=220)
    date_created = models.DateField
    owner = models.ForeignKey(CustomUser,
                              related_name='owned_fleets',
                              on_delete=models.CASCADE)
    supervisor = models.ForeignKey(CustomUser,
                                   related_name='supervised_fleets',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Brand(models.Model):
    Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


class Merchant(models.Model):
    Name = models.CharField(max_length=200, default='Other/Ander')
    latitude = models.DecimalField(decimal_places=2, max_digits=10)
    longitude = models.DecimalField(decimal_places=2, max_digits=10)
    brand = models.ForeignKey(Brand,
                              related_name='merchants',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Transaction(models.Model):
    unique_id = models.CharField
    client = models.ForeignKey(CustomUser,
                               related_name='client_transactions',
                               on_delete=models.CASCADE)
    time = models.TimeField
    date = models.DateField
    registration_number = models.CharField(max_length=10)
    driver = models.ForeignKey(CustomUser,
                               related_name='driver_transactions',
                               on_delete=models.CASCADE)
    cycle_end_date = models.DateField
    brand = models.ForeignKey(Brand,
                              related_name='brand_transactions',
                              on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    merchant = models.ForeignKey(Merchant,
                                 related_name='merchant_transactions',
                                 on_delete=models.CASCADE)
    odo_reading = models.IntegerField
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    fleet = models.ForeignKey(Fleet,
                              related_name='fleet_transactions',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaction ID: {self.pk}, Reg no: {self.registration_number},  Date: {self.date}, Time: {self.time}," \
               f" Quantity: {self.quantity}L, Amount: R{self.amount}."



