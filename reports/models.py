import matplotlib
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
from vehicles.models import Vehicle
from transactions.models import Transaction
from fleet.models import Fleet
from transactions import TransData
import pandas as pd
import matplotlib.pyplot as plt
import logging
from . import ReportUtils

logger = logging.getLogger(__name__)


class GeneralReport:
    @classmethod
    def detailed(cls, fleet_id):
        fleet = Fleet.fleets.get(id=fleet_id)
        vehicles = Vehicle.vehicles.filter(fleet=fleet)
        # Turn vehicles queryset into dataframe then add that to the dictionary
        return dict()

    @classmethod
    def basic(cls):
        return dict()

    @classmethod
    def custom(cls):
        return dict()


class SupervisorReport:
    @classmethod
    def detailed(cls, fleet_id, start_date, end_date):
        fleet = Fleet.fleets.get(id=fleet_id)
        selected_transactions = Transaction.transactions.filter(fleet=fleet, date__range=[start_date, end_date])

        supervisor_fuel_stats = SupervisorReport.supervisor_fuel_stats(fleet_id, selected_transactions)
        supervisor_pie_plot = ReportUtils.plotly_plot_pie(supervisor_fuel_stats, "Supervisor Fuel Stats",
                                                          'Poured (L)', "Supervisor", 800, 800)

        test_line_plot = ReportUtils.plotly_line_plot_test(
            SupervisorReport.supervisor_monthly_stats(fleet_id, selected_transactions),
            "Supervisor fuel stats over time", height=800, width=800)

        supervisor_monthly_stats = ReportUtils.plotly_plot_line(
            SupervisorReport.supervisor_monthly_stats(fleet_id, selected_transactions),
            "Supervisor fuel stats over time", height=800, width=800
        )
        return {"supervisor_fuel_stats": supervisor_fuel_stats,
                "supervisor_pie_plot": supervisor_pie_plot,
                "supervisor_monthly_stats": supervisor_monthly_stats}

    @classmethod
    def basic(cls):
        return dict()

    """Returns a dataframe. Each row is the fuel stats for a supervisor"""

    @classmethod
    def supervisor_fuel_stats(cls, fleet_id, transactions_input):
        fleet = Fleet.fleets.get(id=fleet_id)
        fleet_supervisors = fleet.fleet_supervisors.get_queryset()
        supervisor_data = list()

        for supervisor in fleet_supervisors:

            supervisor_vehicles = supervisor.user.vehicles_added.get_queryset()
            transactions = transactions_input.filter(vehicle__in=supervisor_vehicles)
            transactions_df = TransData.transactions_to_dataframe(transactions)
            poured = transactions_df['quantity'].sum()
            spent = transactions_df['amount'].sum()
            num_transactions = len(transactions_df)
            num_vehicles = len(supervisor_vehicles)
            if num_transactions > 0:
                data = pd.Series([supervisor.user.username, poured, spent, num_transactions, num_vehicles],
                                 index=['Supervisor', 'Poured (L)', 'Spent (R)', 'Number of Transactions',
                                        'Number of Vehicles'])
                supervisor_data.append(data)

        supervisor_data_df = pd.DataFrame(supervisor_data)  # removed index of supervisor names

        return supervisor_data_df

    """Takes in a list of transaction objects"""

    @classmethod
    def supervisor_monthly_stats(cls, fleet_id, transactions_input):
        fleet = Fleet.fleets.get(id=fleet_id)
        fleet_supervisors = fleet.fleet_supervisors.get_queryset()
        stat_list = list()
        display_dates = list()

        """Month, quantity and amount for all transactions. Grouped by month"""
        results = (transactions_input
                   .annotate(transaction_month=TruncMonth('date'))
                   .values('transaction_month')
                   .annotate(poured=Sum("quantity"))
                   .annotate(spent=Sum("amount"))
                   .order_by('transaction_month'))

        for result in results:
            transaction_month = result['transaction_month'].month
            transaction_year = result['transaction_month'].year

            display_date = f"{calendar.month_name[transaction_month]} - {transaction_year}"
            display_dates.append(display_date)
            """Hold amount poured each month by each supervisor"""
            supervisor_poured_stat_list = list()

            for supervisor in fleet_supervisors:
                supervisor_vehicles = supervisor.user.vehicles_added.get_queryset()
                supervisor_transactions = TransData.transactions_to_dataframe(transactions_input
                                                                              .filter(vehicle__in=supervisor_vehicles,
                                                                                      date__month=transaction_month,
                                                                                      date__year=transaction_year
                                                                                      ))
                supervisor_poured_stat_list.append(float(supervisor_transactions['quantity'].sum()))

            stat_list.append(supervisor_poured_stat_list)

        df_columns = list()
        for supervisor in fleet_supervisors:
            df_columns.append(supervisor.user.username)

        stat_df = pd.DataFrame(stat_list, columns=df_columns, index=display_dates)

        return stat_df

    @classmethod
    def custom(cls):
        return dict()


class VehicleReport:
    pass


class StationReport:
    pass


class BrandReport:
    pass


class ModelReport:
    pass
