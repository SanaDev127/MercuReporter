from .views import *
from django.urls import path

urlpatterns = [
    path("create_fleet/", CreateFleet, name='create_fleet'),
    path("add_fleet_supervisor/<int:id>/", add_supervisor, name='add_fleet_supervisor'),
    path("add_fleet_vehicle/", add_vehicle, name='add_fleet_vehicle'),
    path("supervisor_fleet_details/", supervisor_fleet_details, name="supervisor_fleet_details"),
    path("owner_fleet_details/<int:id>/", owner_fleet_details, name="owner_fleet_details"),
    path("add_fleet_vehicle/<int:id>/", add_vehicle, name="add_vehicle"),
    path("add_list_fleet_vehicles/<int:id>/", add_vehicle_list, name="add_vehicle_list"),
    path("add_fleet_merchant/<int:id>/", add_merchant, name="add_merchant"),
    path("add_fleet_brand/<int:id>/", add_brand, name="add_brand"),
]
