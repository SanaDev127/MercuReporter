from django.db import models
from django.contrib.auth.models import AbstractUser
# from vehicles.models import Vehicle
# from transactions.models import Fleet


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
        from transactions.models import Fleet

        owned_fleets = Fleet.fleets.get_queryset().filter(owner=self)
        return fleet in owned_fleets

    def get_owner_fleets(self):
        from transactions.models import Fleet

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


