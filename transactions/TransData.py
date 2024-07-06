import pandas as pd
import numpy as np
from transactions.models import Transaction
from vehicles.models import Vehicle
import logging
from accounts.models import CustomUser

dataframe_columns = ['Client Name', 'Registration No.', 'Driver Name', 'Transaction Description',
                     'Transaction Date', 'Transaction Time', 'Merchant Name', 'Odo Reading', 'Quantity', 'Amount']

logger = logging.getLogger(__name__)


def file_validity_checker(file_path, user):
    file_valid = True
    failure_reason = ""
    # valid_transactions = pd.DataFrame.empty

    try:
        valid_transactions = pd.read_excel(file_path, usecols=dataframe_columns)
    except FileNotFoundError:
        failure_reason = "Transaction File Not Found"
        file_valid = False
    except pd.errors.EmptyDataError:
        failure_reason = "Transaction File is Empty"
        file_valid = False
    except pd.errors.ParserError:
        failure_reason = "Unable To Parse File"
        file_valid = False
    except Exception as e:
        failure_reason = e
        # failure_reason = "Unable To Read File"
        file_valid = False

    # processed_transactions = transaction_dataframe_processor(valid_transactions, user)

    response = {'isValid': file_valid,
                'Reason': failure_reason,
                }

    return response


# Transactions will be checked, if they look funny, they will be highlighted and the user can make changes
# This method will return all invalid transactions (duplicates, deviating odo readings, outrageous prices and quantities

def transaction_dataframe_processor(file_path, user, fleet=None):
    # user = CustomUser(u)
    loaded_transactions = pd.read_excel(file_path)
    grouped_unprocessed_transactions = loaded_transactions.groupby(['Registration No.'])

    duplicate_transactions = list()
    irregular_odo_reading_transactions = list()
    irregular_quantity_amount_transactions = list()
    unregistered_vehicle_transactions = list()
    all_new_transactions = list()

    for vehicle_reg_no in grouped_unprocessed_transactions.groups.keys():
        new_vehicle_df = (grouped_unprocessed_transactions.get_group(vehicle_reg_no))
        new_vehicle_transactions = list()
        for index, row in new_vehicle_df.iterrows():

            transaction_data = pd.Series([row["Client Name"], row["Registration No."], row["Driver Name"],
                                          row["Model Description"], row["Cycle End Date"], row["Brand Description"],
                                          row["Transaction Date"], row["Transaction Time"], row['Merchant Name'],
                                          row['Odo Reading'], row['Quantity'], row['Amount']],
                                         index=["client", "registration_number", "driver", "description",
                                                "cycle_end_date", "brand", "date", "time", "merchant", "odo_reading",
                                                "quantity", "amount"])
            new_vehicle_transactions.append(transaction_data)
            data = [row["Client Name"], row["Registration No."], row["Driver Name"],
                    row["Model Description"], str(row["Cycle End Date"]), row["Brand Description"],
                    str(row["Transaction Date"]), str(row["Transaction Time"]), row['Merchant Name'],
                    row['Odo Reading'], row['Quantity'], row['Amount']]
            all_new_transactions.append(data)

        all_vehicle_transactions = transactions_to_series_list(Transaction.vehicles.get_queryset(vehicle_reg_no))

        duplicates = transaction_duplicate_checker(new_vehicle_transactions, vehicle_reg_no)
        for dupe in duplicates:
            duplicate_transactions.append(dupe)

        irregular_odo = transaction_odo_reading_checker(all_vehicle_transactions, new_vehicle_transactions)
        for odo in irregular_odo:
            irregular_odo_reading_transactions.append(odo)

        irregular_quants = transaction_quantity_amount_checker(all_vehicle_transactions, new_vehicle_transactions)
        for quant in irregular_quants:
            irregular_quantity_amount_transactions.append(quant)

        if user.is_supervisor():
            fleet = user.get_supervisor_fleet()

        unregistered = unregistered_vehicle_checker(new_vehicle_transactions, fleet)
        for trans in unregistered:
            unregistered_vehicle_transactions.append(trans)

    return {'duplicates': duplicate_transactions,
            'irregular_odo_readings': irregular_odo_reading_transactions,
            'irregular_quantity_amounts': irregular_quantity_amount_transactions,
            'all_new_transactions': all_new_transactions,
            'unregistered_vehicle_transactions': unregistered_vehicle_transactions
            }


def transactions_to_series_list(transaction_objects):  # Converts queryset of objects to list of series
    transaction_list = list()
    for trans_object in transaction_objects:
        trans_data = pd.Series([trans_object.client, trans_object.time, trans_object.date,
                                trans_object.registration_number, trans_object.driver, trans_object.cycle_end_date,
                                trans_object.brand, trans_object.description, trans_object.merchant,
                                trans_object.odo_reading, trans_object.quantity, trans_object.amount, trans_object.fleet
                                ], index=["client", "time", "date", "registration_number", "driver", "cycle_end_date",
                                          "brand", "description", "merchant", "odo_reading", "quantity", "amount",
                                          "fleet"])
        transaction_list.append(trans_data)
    return transaction_list


def transaction_duplicate_checker(transactions, registration_no):
    duplicate_transactions = list()
    # If necessary, only get transactions 
    saved_vehicle_transactions = Transaction.vehicles.get_queryset(registration_no)

    for transaction in transactions:
        if saved_vehicle_transactions.filter(
                date=transaction["date"],
                time=transaction["time"],
                odo_reading=transaction["odo_reading"],
                quantity=transaction["quantity"],
                amount=transaction["amount"]
        ):
            duplicate_transactions.append(transaction)

    return duplicate_transactions


def transaction_odo_reading_checker(all_vehicle_transactions, new_vehicle_transactions):
    irregular_odo_reading_transactions = list()

    if all_vehicle_transactions and len(all_vehicle_transactions) > 2:
        vehicle_transactions_df = pd.DataFrame(all_vehicle_transactions)  # Making a df out of list of series
        all_odo_readings = np.array(vehicle_transactions_df['odo_reading'])
        avg_odo_increase = avg_dist_calc(all_odo_readings)

        last_valid_odo_reading = all_odo_readings[-1]
        for trans in new_vehicle_transactions:
            if (trans['odo_reading'] - last_valid_odo_reading) > avg_odo_increase * 3:
                irregular_odo_reading_transactions.append(trans)
            else:
                last_valid_odo_reading = trans['odo_reading']

    return irregular_odo_reading_transactions


def transaction_quantity_amount_checker(all_vehicle_transactions, new_vehicle_transactions):
    irregular_quantity_amount_transactions = list()
    if all_vehicle_transactions and len(all_vehicle_transactions) > 2:
        vehicle_transactions_df = pd.DataFrame(all_vehicle_transactions)
        all_fuel_quantities = np.array(vehicle_transactions_df['quantity'])
        all_fuel_amounts = np.array(vehicle_transactions_df['amount'])

        avg_fuel_price = all_fuel_amounts.mean() / all_fuel_quantities.mean()
        for trans in new_vehicle_transactions:
            if (trans['amount'] / trans['quantity'] > 1.3 * avg_fuel_price or
                    trans['amount'] / trans['quantity'] < 1.3 * avg_fuel_price):
                irregular_quantity_amount_transactions.append(trans)

    return irregular_quantity_amount_transactions


def avg_dist_calc(data_points):
    distances = list()
    for i in range(0, data_points.size):
        dist = data_points[i + 1] - data_points[i]
        distances.append(dist)
    avg_dist = np.mean(distances)
    return avg_dist


def vehicle_in_fleet(reg_no, fleet):
    vehicle = Vehicle.vehicles.get_queryset().filter(registration_number=reg_no)
    if vehicle:
        if vehicle.fleet == fleet:
            return True
        else:
            return False
    else:
        return False


def unregistered_vehicle_checker(new_vehicle_transactions, fleet):
    unregistered = list()
    for trans in new_vehicle_transactions:
        if vehicle_in_fleet(trans['registration_number'], fleet):
            pass
        else:
            unregistered.append(trans)
    return unregistered


# takes in a dataframe representing a single vehicle's transactions and returns the distance it travelled
def calculate_vehicle_distance_travelled(vehicle_transactions):
    distance = (np.array(vehicle_transactions["odo_reading"]).max() - np.array(vehicle_transactions["odo_reading"]).min())
    return float(distance)


def calculate_vehicle_amount_spent(v_transactions):
    vehicle_transactions = pd.DataFrame(v_transactions)
    spent = np.array(vehicle_transactions["amount"]).sum()
    return float(spent)


def calculate_vehicle_amount_poured(v_transactions):
    vehicle_transactions = pd.DataFrame(v_transactions)
    poured = np.array(vehicle_transactions["quantity"]).sum()
    return float(poured)
