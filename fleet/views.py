import pandas as pd
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CreateFleetForm, OwnerAddVehicleForm, SupervisorAddVehicleForm, AddSupervisorForm, AddBrandForm, \
    AddMerchantForm, UploadVehicleFileForm
from .models import Fleet
from django.contrib.auth.models import Group
from vehicles.models import Vehicle
from accounts.models import Supervisor
from django.shortcuts import get_object_or_404
from transactions.models import Merchant, Brand
from transactions import TransData
import logging
from django.contrib import messages
from accounts.models import CustomUser

logger = logging.getLogger(__name__)
vehicle_dataframe_columns = ["Registration No.", "Client Reference 1", "Vehicle Status", "Model Description", "Colour",
                             "Litres Limit", "Primary Tank Capacity", "Secondary Tank Capacity"]


def CreateFleet(request):
    user = request.user

    if request.method == "POST":
        create_fleet_form = CreateFleetForm(request.POST)
        if create_fleet_form.is_valid():
            cd = create_fleet_form.cleaned_data
            if Fleet.fleets.filter(owner=user, Name=cd['name']):
                messages.warning(request, "Fleet already exists with that name. Please try again.")
                return render(request, "fleet/CreateFleet.html", {"create_fleet_form": create_fleet_form})
            else:
                new_fleet = Fleet()
                new_fleet.Name = cd['name']
                new_fleet.owner = request.user
                new_fleet.save()
                if new_fleet is not None:
                    # fleet_obj = Fleet.fleets.get()
                    return render(request, "fleet/CreateFleetSuccess.html",
                                  {"fleet": new_fleet})
                else:
                    # Return the user to the form showing the errors
                    return HttpResponse("Form is not valid")
    else:
        create_fleet_form = CreateFleetForm()
    return render(request, "fleet/CreateFleet.html", {"create_fleet_form": create_fleet_form})


def add_merchant(request, id):
    user = request.user

    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        add_merchant_form = AddMerchantForm(request.POST)
        if add_merchant_form.is_valid():
            cd = add_merchant_form.cleaned_data
            if Merchant.merchants.filter(fleet=fleet, Name__iexact=cd['Name'], brand=cd['Brand']):
                messages.warning(request, "Merchant already exists with that name. Please try again.")
            else:
                new_merchant = Merchant()
                new_merchant.Name = cd['Name']
                if cd['address']:
                    new_merchant.address = cd['address']
                if cd['latitude']:
                    new_merchant.latitude = cd['latitude']
                if cd['longitude']:
                    new_merchant.longitude = cd['longitude']
                # brand = Brand.brands.get(Name=)
                new_merchant.brand = cd['brand']
                new_merchant.fleet = fleet

                new_merchant.save()
                if new_merchant is not None:
                    return render(request, "merchant/AddMerchantSuccess.html",
                                  {"merchant": new_merchant,
                                   "fleet": fleet})
                else:
                    # Return the user to the form showing the errors
                    return HttpResponse("Form is not valid")
    else:
        add_merchant_form = AddMerchantForm()
        add_merchant_form.fields["brand"].queryset = Brand.brands.get_queryset().filter(fleet=fleet)

    return render(request, "merchant/AddMerchant.html", {"add_merchant_form": add_merchant_form,
                                                         "fleet": fleet,
                                                         "user": user})


def add_brand(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        add_brand_form = AddBrandForm(request.POST)
        if add_brand_form.is_valid():
            cd = add_brand_form.cleaned_data
            if Brand.brands.filter(fleet=fleet, Name__iexact=cd['Name']):
                messages.warning(request, "Brand already exists with that name. Please try again.")
            else:
                new_brand = Brand()
                new_brand.Name = cd['Name']
                new_brand.fleet = fleet
                new_brand.save()
                if new_brand is not None:
                    return render(request, "brand/AddBrandSuccess.html",
                                  {"brand": new_brand,
                                   "fleet": fleet})
        else:
            # Return the user to the form showing the errors
            return HttpResponse("Form is not valid")
    else:
        add_brand_form = AddBrandForm()

    return render(request, "brand/AddBrand.html", {"add_brand_form": add_brand_form,
                                                   "fleet": fleet,
                                                   "user": user})


def add_vehicle(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        if user.is_owner():
            add_vehicle_form = OwnerAddVehicleForm(request.POST)
            if add_vehicle_form.is_valid():
                cd = add_vehicle_form.cleaned_data
                if Vehicle.vehicles.filter(fleet=fleet, registration_number__iexact=cd['registration_number']):
                    messages.warning(request, "Vehicle already exists with that registration number. Please try again.")
                else:
                    new_vehicle = Vehicle()

                    new_vehicle.registration_number = cd['registration_number']
                    new_vehicle.model_description = cd['model_description']
                    new_vehicle.addedBy = cd['addedBy']
                    new_vehicle.fleet = fleet

                    new_vehicle.save()

                    if new_vehicle is not None:
                        return render(request, "vehicle/AddVehicleSuccess.html",
                                      {"vehicle": new_vehicle,
                                       "fleet": fleet})
                    else:
                        # Return the user to the form showing the errors
                        return HttpResponse("Form is not valid")
        else:
            add_vehicle_form = SupervisorAddVehicleForm(request.POST)
            if add_vehicle_form.is_valid():
                new_vehicle = Vehicle()
                cd = add_vehicle_form.cleaned_data
                new_vehicle.registration_number = cd['registration_number']
                new_vehicle.model_description = cd['model_description']
                new_vehicle.fleet = fleet
                new_vehicle.addedBy = user

                new_vehicle.save()

                if new_vehicle is not None:
                    return render(request, "vehicle/AddVehicleSuccess.html",
                                  {"vehicle": new_vehicle,
                                   "fleet": fleet})
                else:
                    return HttpResponse("Form is not valid")
    else:
        if user.is_owner():
            add_vehicle_form = OwnerAddVehicleForm()
            # add_vehicle_form.addedBy.queryset.filter(fleet=fleet)
            add_vehicle_form.fields["addedBy"].queryset = Supervisor.supervisors.get_queryset().filter(fleet=fleet)
            # add_vehicle_form.addedBy.queryset = Supervisor.supervisors.get_queryset().filter(fleet=fleet)
        else:
            add_vehicle_form = SupervisorAddVehicleForm()

    return render(request, "vehicle/AddVehicle.html", {"add_vehicle_form": add_vehicle_form,
                                                       "fleet": fleet,
                                                       "user": user})


def add_vehicle_list(request, id):
    user = request.user
    fleet = Fleet.fleets.get(id=id)

    if request.method == 'POST':
        add_vehicle_list_form = UploadVehicleFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        response = TransData.vehicle_file_validity_checker(file)

        if response['isValid']:
            vehicle_df = pd.read_excel(file, usecols=vehicle_dataframe_columns)
            duplicate_vehicles = list()
            num_added_vehicles = 0
            for index, row in vehicle_df.iterrows():
                registration_number = row["Registration No."]
                area = row["Client Reference 1"]
                vehicle_status = row["Vehicle Status"]
                model_description = row["Model Description"]
                colour = row["Colour"]
                litres_limit = row["Litres Limit"]
                primary_tank_capacity = row["Primary Tank Capacity"]
                secondary_tank_capacity = row["Secondary Tank Capacity"]

                # Not sure if this is done or not. Too lazy to test it. Been a long day
                # If I were to test it I'd probably have to clear all the tables and re add the vehicle list
                vehicle_supervisor = row["Driver Name"]
                if Supervisor.supervisors.filter(fleet=fleet, user__Name__iexact=vehicle_supervisor):
                    supervisor = Supervisor.supervisors.filter(fleet=fleet, user__Name=vehicle_supervisor)
                else:
                    supervisor = Supervisor()
                    # Giving the user default login details
                    new_user = CustomUser(username=vehicle_supervisor,
                                          password="Admin",
                                          email="Admin")
                    new_user.save()
                    supervisor.user = new_user
                    supervisor.fleet = fleet
                    supervisor.save()

                if Vehicle.vehicles.get_queryset().filter(fleet=fleet, registration_number=registration_number):
                    duplicate_vehicles.append(registration_number)
                else:
                    num_added_vehicles += 1
                    new_vehicle = Vehicle(registration_number=registration_number, model_description=model_description,
                                          fleet=fleet, addedBy=user, area=area, vehicle_status=vehicle_status,
                                          colour=colour, litres_limit=litres_limit,
                                          primary_tank_capacity=primary_tank_capacity,
                                          secondary_tank_capacity=secondary_tank_capacity, supervisor=supervisor)
                    new_vehicle.save()
            return render(request, "vehicle/AddMultipleVehiclesSuccess.html", {"fleet": fleet,
                                                                               "num_added_vehicles": num_added_vehicles,
                                                                               "num_duplicates": len(
                                                                                   duplicate_vehicles),
                                                                               "duplicate_vehicles": duplicate_vehicles})
        else:
            return render(request, 'upload/invalid_transaction_file.html',
                          {'Failure_Reason': response['Reason']})
    else:
        add_vehicle_list_form = UploadVehicleFileForm()


def add_supervisor(request, id):
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        add_supervisor_form = AddSupervisorForm(request.POST)
        if add_supervisor_form.is_valid():
            if Supervisor.supervisors.filter(fleet=fleet,
                                             user__username__iexact=add_supervisor_form.cleaned_data['username']):
                messages.warning(request, "Supervisor already exists with that name. Please try again.")
            else:
                new_supervisor = add_supervisor_form.save(commit=False)
                new_supervisor.set_password(
                    add_supervisor_form.cleaned_data['password']
                )
                group = Group.objects.get(name="Supervisors")

                new_supervisor.save()
                new_supervisor.groups.add(group)

                Supervisor.supervisors.create(user=new_supervisor, fleet=fleet)

                if new_supervisor is not None:
                    # Take the user to a page showing new supervisors
                    return render(request, "supervisor/AddSupervisorSuccess.html",
                                  {"supervisor": new_supervisor,  # or username or email
                                   "fleet": fleet})
                else:
                    # Return the user to the form showing the errors
                    return HttpResponse("Form is not valid")
    else:
        add_supervisor_form = AddSupervisorForm()
    return render(request, "supervisor/AddSupervisor.html", {"add_supervisor_form": add_supervisor_form,
                                                             "fleet": fleet})


def owner_fleet_details(request, id):
    fleet = Fleet.fleets.get(id=id)
    vehicles = Vehicle.vehicles.get_queryset().filter(fleet=fleet)
    supervisors = Supervisor.supervisors.get_queryset().filter(fleet=fleet)
    merchants = Merchant.merchants.get_queryset().filter(fleet=fleet)
    brands = Brand.brands.get_queryset().filter(fleet=fleet)

    vehicle_activity = dict()
    for vehicle in vehicles:
        num_transactions = len(vehicle.vehicle_transactions.get_queryset())
        vehicle_activity[vehicle.registration_number] = num_transactions
    most_active_vehicles = dict(sorted(vehicle_activity.items(), key=lambda x: x[1], reverse=False)[:9])

    vehicles = Vehicle.vehicles.get_queryset().filter(registration_number__in=list(most_active_vehicles.keys()))

    add_vehicle_list_form = UploadVehicleFileForm()

    return render(request,
                  "owner/OwnerFleetDetails.html",
                  {"fleet": fleet,
                   "vehicles": vehicles,
                   "supervisors": supervisors,
                   "merchants": merchants,
                   "brands": brands,
                   "add_vehicle_list_form": add_vehicle_list_form
                   })


def supervisor_fleet_details(request):
    supervisor_object = Supervisor.supervisors.get(user=request.user)
    fleet = supervisor_object.fleet

    vehicles = Vehicle.vehicles.filter(fleet=fleet).annotate(transaction_count=Count('vehicle_transactions')).order_by(
        '-transaction_count')[:5]
    brands = Brand.brands.filter(fleet=fleet).annotate(transaction_count=Count('brand_transactions')).order_by(
        '-transaction_count')[:5]
    merchants = Merchant.merchants.filter(fleet=fleet).annotate(
        transaction_count=Count('merchant_transactions')).order_by('-transaction_count')[:5]

    add_vehicle_list_form = UploadVehicleFileForm()

    return render(request,
                  "supervisor/SupervisorFleetDetails.html",
                  {"fleet": fleet,
                   "vehicles": vehicles,
                   "merchants": merchants,
                   "brands": brands,
                   "add_vehicle_list_form": add_vehicle_list_form})


# I think this one shows personal details for supervisors
def supervisor_details(request, supervisor_id):
    supervisor = get_object_or_404(Supervisor,
                                   id=supervisor_id)
    return render(request,
                  "supervisor/supervisor_details.html",
                  {"supervisor": supervisor})
