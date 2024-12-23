import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadTransactionFileForm, ScanTransactionForm, FilterTransactionDateForm
from transactions import TransData
from .models import Transaction
import logging
from accounts.models import Supervisor
from fleet.models import Fleet
from datetime import datetime
from transactions.models import Merchant, Brand
from vehicles.models import Vehicle

logger = logging.getLogger(__name__)


def upload_transaction_file(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)
    if request.method == 'POST':
        form = UploadTransactionFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        # Give file to uploading methods
        response = TransData.file_validity_checker(file)

        if response['isValid']:
            if user.is_owner():
                # The owner is going to select a fleet to add transactions for,
                # that is going to be sent through the request when they use this
                results = TransData.transaction_dataframe_processor(file, user, request.session.get('fleet'))
            else:
                results = TransData.transaction_dataframe_processor(file, user)

            duplicate_transactions = results['duplicates']
            irregular_odo_reading_transactions = results['irregular_odo_readings']
            irregular_quantity_or_amount_transactions = results['irregular_quantity_amounts']
            unregistered_vehicle_transactions = results['unregistered_vehicle_transactions']
            all_new_transactions = results['all_new_transactions']

            request.session['all_new_transactions'] = all_new_transactions

            return render(request, 'upload/check_upload_details.html',
                          {'duplicates': duplicate_transactions,
                           'irregular_odo_readings': irregular_odo_reading_transactions,
                           'irregular_quantity_amount': irregular_quantity_or_amount_transactions,
                           'num_dupes': len(duplicate_transactions),
                           'num_odo': len(irregular_odo_reading_transactions),
                           'num_quants': len(irregular_quantity_or_amount_transactions),
                           'unregistered_vehicle_transactions': unregistered_vehicle_transactions,
                           'fleet': fleet
                           },
                          )

        else:
            return render(request, 'upload/invalid_transaction_file.html',
                          {'Failure_Reason': response['Reason']})

            # Depending on result of the upload, return user to specific template

    else:
        form = UploadTransactionFileForm()


def preview_transaction_effects(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)
    transactions = request.session.get('all_new_transactions')
    transaction_df = pd.DataFrame(transactions, columns=["client", "registration_number", "driver", "description",
                                                         "cycle_end_date", "brand", "date", "time", "merchant",
                                                         "odo_reading",
                                                         "quantity", "amount"])
    grouped_transaction_df = transaction_df.groupby(['registration_number'])

    results = list()

    for vehicle_reg_no in grouped_transaction_df.groups.keys():
        new_vehicle_transactions = grouped_transaction_df.get_group(vehicle_reg_no)
        distance_travelled = round(float(TransData.calculate_vehicle_distance_travelled(new_vehicle_transactions)), 2)
        amount_spent = round(float(TransData.calculate_vehicle_amount_spent(new_vehicle_transactions)), 2)
        amount_poured = round(float(TransData.calculate_vehicle_amount_poured(new_vehicle_transactions)), 2)

        saved_vehicle_transactions = pd.DataFrame(
            TransData.transactions_to_series_list(
                Transaction.vehicles.get_queryset(vehicle_reg_no)
            )
        )

        if not saved_vehicle_transactions.empty:
            previous_distance_travelled = round(
                float(TransData.calculate_vehicle_distance_travelled(saved_vehicle_transactions)), 2)
            previous_amount_spent = round(
                float(TransData.calculate_vehicle_amount_spent(saved_vehicle_transactions)), 2)
            previous_amount_poured = round(
                float(TransData.calculate_vehicle_amount_poured(saved_vehicle_transactions)), 2)
        else:
            previous_distance_travelled = 0
            previous_amount_spent = 0
            previous_amount_poured = 0

        new_distance_travelled = distance_travelled + previous_distance_travelled
        new_amount_spent = amount_spent + previous_amount_spent
        new_amount_poured = amount_poured + previous_amount_poured

        data = pd.Series([vehicle_reg_no,
                          distance_travelled, previous_distance_travelled, new_distance_travelled,
                          amount_poured, previous_amount_poured, new_amount_poured,
                          amount_spent, previous_amount_spent, new_amount_spent],
                         index=['vehicle_reg_no',
                                'distance_travelled', 'previous_distance_travelled', 'new_distance_travelled',
                                'amount_poured', 'previous_amount_poured', 'new_amount_poured',
                                'amount_spent', 'previous_amount_spent', 'new_amount_spent'])
        results.append(data)
    request.session["approved_transactions"] = transactions
    # request.transactions = transactions
    return render(request, "upload/view_upload_effects.html", {'results': results,
                                                               'fleet': fleet})


def save_transaction_file_upload(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)
    if user.is_owner():
        client = user

    else:
        supervisor = Supervisor.supervisors.get(user=user)
        client = supervisor.fleet.owner

    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    date_time_format = '%Y-%m-%d %H:%M:%S'

    transaction_list = request.session.get('approved_transactions')  # list of lists. Each list is a transaction
    num_transactions = len(transaction_list)
    for transaction in transaction_list:
        registration_number = transaction[1]
        cycle_end_date = datetime.strptime(transaction[4], date_time_format).date()
        brand_name = transaction[5]
        date = datetime.strptime(transaction[6], date_time_format).date()
        time = datetime.strptime(transaction[7], time_format).time()
        vehicle = Vehicle.vehicles.get(fleet=fleet, registration_number=registration_number)

        merchant_name = transaction[8]
        if Merchant.merchants.filter(fleet=fleet, Name__iexact=merchant_name):
            merchant = Merchant.merchants.get(fleet=fleet, Name=merchant_name)
            brand = merchant.brand
        else:

            if Brand.brands.filter(fleet=fleet, Name__iexact=brand_name):
                brand = Brand.brands.get(fleet=fleet, Name=brand_name)
                merchant = Merchant(Name=merchant_name, brand=brand, fleet=fleet)
                merchant.save()
            else:
                brand = Brand(Name=brand_name, fleet=fleet)
                brand.save()
                merchant = Merchant(Name=merchant_name, brand=brand, fleet=fleet)
                merchant.save()

        odo_reading = transaction[9]
        quantity = transaction[10]
        amount = transaction[11]

        new_transaction = Transaction(client=client, time=time, date=date, registration_number=registration_number,
                                      brand=brand, merchant=merchant, odo_reading=odo_reading, quantity=quantity,
                                      amount=amount, fleet=fleet, addedBy=user, vehicle=vehicle)
        new_transaction.save()

    return render(request, "upload/upload_transaction_file_success.html", {"user": user,
                                                                           "fleet": fleet,
                                                                           "num_transactions": num_transactions})


def transaction_list(request, id):
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        form = FilterTransactionDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start_date']
            end_date = cd['end_date']
            # form = FilterTransactionDateForm()
            transactions = Transaction.transactions.filter(fleet=fleet, date__range=[start_date, end_date])
            return render(request, "view/transaction_list.html", {"transactions": transactions,
                                                                  "fleet": fleet,
                                                                  "form": form,
                                                                  "num_transactions": len(transactions)})
        else:
            return HttpResponse("Invalid Date Input")
    else:
        form = FilterTransactionDateForm()
    return render(request, "view/transaction_list.html", {"form": form,
                                                          "fleet": fleet})


def scan_transaction_receipt(request):
    if request.method == 'POST':
        form = ScanTransactionForm(request.POST, request.FILES)
        file = request.FILES['file']
        # Give file to uploading methods
        # Depending on result of the upload, return user to specific template
    else:
        form = ScanTransactionForm()
