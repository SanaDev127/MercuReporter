import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from transactions.forms import UploadTransactionFileForm, ScanTransactionForm
from django.http import HttpResponse
from transactions import TransData


def user_dashboard(request):
    user = request.user
    if user.is_driver():
        return render(request,
                      'dashboards/driver_dashboard.html',
                      {'user': user})
    elif user.is_supervisor():
        return render(request,
                      'dashboards/supervisor_dashboard.html',
                      {'user': user})
    elif user.is_owner():
        return render(request,
                      'dashboards/owner_dashboard.html',
                      {'user': user})


def transaction_dashboard(request):
    user = request.user
    if user.is_driver():
        transaction_upload_form = UploadTransactionFileForm()
        transaction_scan_form = ScanTransactionForm()
        return render(request,
                      'dashboards/transactions/driver_transactions.html',
                      {'user': user,
                       'upload_transaction_file_form': transaction_upload_form,
                       'scan_transaction_file_form': transaction_scan_form})
    elif user.is_supervisor():
        transaction_upload_form = UploadTransactionFileForm()
        transaction_scan_form = ScanTransactionForm()
        return render(request,
                      'dashboards/transactions/supervisor_transactions.html',
                      {'user': user,
                       'upload_transaction_file_form': transaction_upload_form,
                       'scan_transaction_file_form': transaction_scan_form})
    elif user.is_owner():
        return render(request,
                      'dashboards/transactions/owner_transactions.html',
                      {'user': user})


def analytics_dash(request):
    user = request.user
    if user.is_driver():
        return render(request,
                      'dashboards/analytics/driver_analytics.html',
                      {'user': user})
    elif user.is_supervisor():
        return render(request,
                      'dashboards/analytics/supervisor_analytics.html',
                      {'user': user})
    elif user.is_owner():
        return render(request,
                      'dashboards/analytics/owner_analytics.html',
                      {'user': user})


def fleet_dash(request):
    user = request.user
    if user.is_owner():
        return render(request,
                      'dashboards/fleet/owner_fleets.html',
                      {'user': user})
    elif user.is_supervisor():
        return render(request,
                      'dashboards/fleet/supervisor_fleet.html',
                      {'user': user})


def vehicle_dash(request):
    user = request.user
    return render(request,
                  'dashboards/vehicle/driver_vehicle_dash.html')


class HomePageView(TemplateView):
    template_name = "home.html"
