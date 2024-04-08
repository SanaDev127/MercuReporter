from django.urls import path
from .views import HomePageView, driver_dashboard, owner_dashboard, supervisor_dashboard, upload_transaction_file

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("drivers/", driver_dashboard, name='driver_dashboard'),
    path("owners/", owner_dashboard, name='owner_dashboard'),
    path("supervisors/", supervisor_dashboard, name='supervisor_dashboard'),
    path("transaction_upload/", upload_transaction_file, name='transaction_upload'),
]