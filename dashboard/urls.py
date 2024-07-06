from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("users/", user_dashboard, name='user_dashboards'),
    path("transactions/", transaction_dashboard, name='transaction_dashboards'),
    path("analytics/", analytics_dash, name='analytics_dashboards'),
    path("fleet/", fleet_dash, name='fleet_dashboards'),
    path("vehicle/", vehicle_dash, name='vehicle_dashboard'),
]
