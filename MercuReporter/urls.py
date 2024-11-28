
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboards/", include("dashboard.urls")),
    path("transactions/", include("transactions.urls")),
    path("fleets/", include("fleet.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("reports/", include("reports.urls")),
    path("", include("dashboard.urls")),


]
