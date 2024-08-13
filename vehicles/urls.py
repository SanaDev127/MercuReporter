from .views import *
from django.urls import path

urlpatterns = [
    path("vehicle_list/<int:id>/", vehicle_list, name='vehicle_list'),

]

