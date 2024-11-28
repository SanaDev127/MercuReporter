from .views import *
from django.urls import path

urlpatterns = [
    path("detailed_supervisor_report/<int:id>/", detailed_supervisor_report, name='detailed_supervisor_report'),
]

