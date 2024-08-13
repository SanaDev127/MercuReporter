from django.db import models
from transactions.models import Fleet
from accounts.models import CustomUser


class VehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=250)
    model_description = models.CharField(max_length=250)
    fleet = models.ForeignKey(Fleet,
                              related_name='fleet_vehicles',
                              on_delete=models.CASCADE)
    driver = models.ForeignKey(CustomUser,
                               related_name='driver_vehicles',
                               null=True,
                               on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    addedBy = models.ForeignKey(CustomUser,
                                related_name='vehicles_added',
                                null=True,
                                on_delete=models.SET_NULL)
    area = models.CharField(max_length=250, null=True)
    vehicle_status = models.CharField(max_length=20, null=True)
    colour = models.CharField(max_length=30, null=True)
    litres_limit = models.IntegerField(null=True)
    primary_tank_capacity = models.IntegerField(null=True)
    secondary_tank_capacity = models.IntegerField(null=True)

    vehicles = VehicleManager()

    def __str__(self):
        return self.registration_number
