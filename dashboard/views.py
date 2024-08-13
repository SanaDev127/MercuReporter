from datetime import datetime
import calendar
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

import fleet.views
from transactions.forms import UploadTransactionFileForm, ScanTransactionForm
from fleet.models import Fleet
from vehicles.models import Vehicle
from transactions.models import Transaction
from accounts.models import Supervisor
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
        supervisor = Supervisor.supervisors.get(user=user)
        fleet = supervisor.fleet

        transaction_upload_form = UploadTransactionFileForm()
        transaction_scan_form = ScanTransactionForm()
        # Showing stats for previous month because most likely won't be getting realtime data
        # previous_month = calendar.month_name[datetime.now().month - 1]
        latest_transactions = Transaction.transactions.get_queryset().filter(fleet=fleet).order_by('-date')[:10]
        latest_transaction = latest_transactions[:1].get()
        current_year = latest_transaction.date.year
        latest_month = latest_transaction.date.month
        summary_stats = TransData.fleet_summary_stats(fleet.id, current_year, latest_month)

        return render(request,
                      'dashboards/transactions/supervisor_transactions.html',
                      {'user': user,
                       "fleet": fleet,
                       'upload_transaction_file_form': transaction_upload_form,
                       "latest_month": calendar.month_name[latest_transaction.date.month],
                       'scan_transaction_file_form': transaction_scan_form,
                       "num_transactions": summary_stats["num_transactions"],
                       "avg_fuel_price": summary_stats["avg_fuel_price"],
                       "largest_transaction": summary_stats["largest_transaction"],
                       "smallest_transaction": summary_stats["smallest_transaction"],
                       "latest_transactions": latest_transactions,
                       })
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
        created_fleets = Fleet.fleets.get_queryset().filter(owner=user)
        return render(request,
                      'dashboards/fleet/owner_fleets.html',
                      {'user': user,
                       'created_fleets': created_fleets})
    elif user.is_supervisor():

        return redirect(fleet.views.supervisor_fleet_details)


def vehicle_dash(request):
    user = request.user
    return render(request,
                  'dashboards/vehicle/driver_vehicle_dash.html')


class HomePageView(TemplateView):
    template_name = "home.html"
