import pandas as pd
from django.shortcuts import render, redirect, reverse
from .forms import UploadTransactionFileForm, ScanTransactionForm
from django.http import HttpResponse
from transactions import TransData
from .models import Transaction
import logging

logger = logging.getLogger(__name__)


def upload_transaction_file(request):
    user = request.user
    if request.method == 'POST':
        form = UploadTransactionFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        # Give file to uploading methods
        response = TransData.file_validity_checker(file, user)

        if response['isValid']:
            if user.is_owner():
                # The owner is going to select a fleet to add transactions for,
                # that is going to be sent through the request when they use this
                results = TransData.transaction_dataframe_processor(file, user, request['fleet'])
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
                           'unregistered_vehicle_transactions': unregistered_vehicle_transactions
                           },
                          )

        else:
            return render(request, 'upload/invalid_transaction_file.html',
                          {'Failure_Reason': response['Reason']})

            # Depending on result of the upload, return user to specific template

    else:
        form = UploadTransactionFileForm()


def preview_transaction_effects(request):
    user = request.user
    transactions = request.session.get('all_new_transactions')  # request.all_new_transactions/request.get('all_new_transactions')
    transaction_df = pd.DataFrame(transactions, columns=["client", "registration_number", "driver", "description",
                                                         "cycle_end_date", "brand", "date", "time", "merchant",
                                                         "odo_reading",
                                                         "quantity", "amount"])
    grouped_transaction_df = transaction_df.groupby(['registration_number'])

    results = list()

    for vehicle_reg_no in grouped_transaction_df.groups.keys():
        new_vehicle_transactions = grouped_transaction_df.get_group(vehicle_reg_no)
        distance_travelled = round(float(TransData.calculate_vehicle_distance_travelled(new_vehicle_transactions)),2)
        amount_spent = round(float(TransData.calculate_vehicle_amount_spent(new_vehicle_transactions)),2)
        amount_poured = round(float(TransData.calculate_vehicle_amount_poured(new_vehicle_transactions)),2)

        saved_vehicle_transactions = pd.DataFrame(
            TransData.transactions_to_series_list(
                Transaction.vehicles.get_queryset(vehicle_reg_no)
            )
        )

        if not saved_vehicle_transactions.empty:
            previous_distance_travelled = round(float(TransData.calculate_vehicle_distance_travelled(saved_vehicle_transactions)),2)
            previous_amount_spent = round(float(TransData.calculate_vehicle_amount_spent(saved_vehicle_transactions)),2)
            previous_amount_poured = round(float(TransData.calculate_vehicle_amount_poured(saved_vehicle_transactions)),2)
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

    request.transactions = transactions
    return render(request, "upload/view_upload_effects.html", {'results': results})


def save_transaction_file_upload(request):
    pass


def scan_transaction_receipt(request):
    if request.method == 'POST':
        form = ScanTransactionForm(request.POST, request.FILES)
        file = request.FILES['file']
        # Give file to uploading methods
        # Depending on result of the upload, return user to specific template
    else:
        form = ScanTransactionForm()
