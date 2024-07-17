from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def is_supervisor(self):
        if self.groups.filter(name='Supervisors').exists():
            return True
        else:
            return False

    def is_driver(self):
        if self.groups.filter(name='Drivers').exists():
            return True
        else:
            return False

    def is_owner(self):
        if self.groups.filter(name='Owners').exists():
            return True
        else:
            return False

    def owns_fleet(self, fleet):
        from fleet.models import Fleet

        owned_fleets = Fleet.fleets.get_queryset().filter(owner=self)
        return fleet in owned_fleets

    def get_owner_fleets(self):
        from fleet.models import Fleet

        if self.is_owner():
            owned_fleets = Fleet.fleets.get_queryset().filter(owner=self)
            return owned_fleets
        else:
            return None

    def get_supervisor_fleet(self):
        from transactions.models import Fleet

        if self.is_supervisor():
            fleet = Fleet.fleets.get_queryset().filter(supervisor=self)
            return fleet
        else:
            return None

    def get_driver_vehicle(self):
        from vehicles.models import Vehicle

        if self.is_driver():
            vehicle = Vehicle.vehicles.get_queryset().filter(driver=self)
            return vehicle
        else:
            return None

    def get_driver_fleet(self):
        if self.is_driver():
            vehicle = self.get_driver_vehicle()
            fleet = vehicle.fleet
            return fleet
        else:
            return None


class Owner(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SupervisorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Supervisor(models.Model):
    from fleet.models import Fleet

    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)

    fleet = models.ForeignKey(Fleet,
                              related_name="supervised_fleet",
                              null=True,
                              on_delete=models.SET_NULL)

    supervisors = SupervisorManager()

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

