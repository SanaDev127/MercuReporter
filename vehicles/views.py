import pandas as pd
from django.shortcuts import render
from fleet.models import Fleet
from .models import Vehicle
from transactions import TransData


def vehicle_list(request, id):
    fleet = Fleet.fleets.get(id=id)
    list_vehicles = Vehicle.vehicles.get_queryset().filter(fleet=fleet)
    vehicles = list()
    for vehicle in list_vehicles:
        last_odo_reading = vehicle.vehicle_transactions.get_queryset().order_by('-date').first().odo_reading if vehicle.vehicle_transactions.get_queryset() else 0
        travelled = TransData.calculate_vehicle_distance_travelled(
            TransData.transactions_to_dataframe(vehicle.vehicle_transactions.get_queryset())
        )
        poured = TransData.calculate_vehicle_amount_poured(
            TransData.transactions_to_dataframe(vehicle.vehicle_transactions.get_queryset())
        )

        if poured == 0 or travelled == 0:
            consumption = 0
        else:
            consumption = round((poured / travelled * 100), 2)

        transaction_count = len(vehicle.vehicle_transactions.get_queryset())

        data = pd.Series([vehicle.model_description, vehicle.registration_number, vehicle.vehicle_status,
                          last_odo_reading, consumption, transaction_count],
                         index=["model_description", "registration_number", "status",
                                "last_odo_reading", "consumption", "transaction_count"])
        vehicles.append(data)

    return render(request, "vehicle_list.html", {'vehicles': vehicles,
                                                 "fleet": fleet})
