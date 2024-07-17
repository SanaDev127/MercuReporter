from django.db import models
from accounts.models import CustomUser


class FleetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Fleet(models.Model):
    Name = models.CharField(max_length=220)
    date_created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser,
                              related_name='owned_fleets',
                              on_delete=models.CASCADE)
    """supervisor = models.ForeignKey(CustomUser,
                                   related_name='supervised_fleets',
                                   null=True,
                                   on_delete=models.SET_NULL)"""
    fleets = FleetManager()

    def __str__(self):
        return self.Name



