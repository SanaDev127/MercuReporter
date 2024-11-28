import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from fleet.models import Fleet
from transactions.models import Transaction
from . import ReportUtils
from transactions.forms import FilterTransactionDateForm


def detailed_supervisor_report(request, id):
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        form = FilterTransactionDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start_date']
            end_date = cd['end_date']
            detailed_report = SupervisorReport.detailed(fleet.id, start_date, end_date)

            supervisor_fuel_stats_df = (detailed_report["supervisor_fuel_stats"])
            supervisor_fuel_stats = list()
            for index, row in supervisor_fuel_stats_df.iterrows():
                data = pd.Series([row["Supervisor"], row["Poured (L)"], row["Spent (R)"], row["Number of Transactions"],
                                  row['Number of Vehicles']],
                                 index=["supervisor", "poured", "spent", "num_transactions", "num_vehicles"])
                supervisor_fuel_stats.append(data)
            supervisor_pie_plot = detailed_report["supervisor_pie_plot"]
            return render(request, "supervisor/generate_detailed_supervisor_report.html",
                          {"supervisor_fuel_stats": supervisor_fuel_stats,
                           "supervisor_pie_plot": supervisor_pie_plot,
                           "fleet": fleet,
                           "form": form})
        else:
            return HttpResponse("Invalid Date Input")
    else:
        form = FilterTransactionDateForm()
    return render(request, "supervisor/generate_detailed_supervisor_report.html", {"form": form,
                                                                                   "fleet": fleet})


def test_plots(request, id):
    fleet = Fleet.fleets.get(id=id)
    transactions_list = Transaction.transactions.filter(fleet=fleet)
    supervisor_report_df = SupervisorReport.supervisor_fuel_stats(id, transactions_list)

    supervisor_line_plot = ReportUtils.plot_line(supervisor_report_df, 10, 10)
    logger.warning(type(supervisor_line_plot))
    return HttpResponse("All Good")
