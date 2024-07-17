from django.http import HttpResponse
from django.shortcuts import render
from .forms import CreateFleetForm, OwnerAddVehicleForm, SupervisorAddVehicleForm, AddSupervisorForm, AddBrandForm, \
    AddMerchantForm
from .models import Fleet
from django.contrib.auth.models import Group
from vehicles.models import Vehicle
from accounts.models import Supervisor
from django.shortcuts import get_object_or_404
from transactions.models import Transaction, Merchant, Brand


def CreateFleet(request):
    user = request.user

    if request.method == "POST":
        create_fleet_form = CreateFleetForm(request.POST)
        if create_fleet_form.is_valid():
            new_fleet = Fleet()
            cd = create_fleet_form.cleaned_data
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
            new_merchant = Merchant()
            cd = add_merchant_form.cleaned_data
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
            new_brand = Brand()
            cd = add_brand_form.cleaned_data
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
                new_vehicle = Vehicle()
                cd = add_vehicle_form.cleaned_data
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


def add_supervisor(request, id):
    fleet = Fleet.fleets.get(id=id)
    if request.method == "POST":
        add_supervisor_form = AddSupervisorForm(request.POST)
        if add_supervisor_form.is_valid():
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

    return render(request,
                  "owner/OwnerFleetDetails.html",
                  {"fleet": fleet,
                   "vehicles": vehicles,
                   "supervisors": supervisors,
                   "merchants": merchants,
                   "brands": brands
                   })


def supervisor_fleet_details(request):
    supervisor_object = Supervisor.supervisors.get(user=request.user)
    fleet = supervisor_object.fleet
    vehicles = Vehicle.vehicles.get_queryset().filter(fleet=fleet)
    merchants = Merchant.merchants.get_queryset().filter(fleet=fleet)
    brands = Brand.brands.get_queryset().filter(fleet=fleet)

    return render(request,
                  "supervisor/SupervisorFleetDetails.html",
                  {"fleet": fleet,
                   "vehicles": vehicles,
                   "merchants": merchants,
                   "brands": brands})


# I think this one shows personal details for supervisors
def supervisor_details(request, supervisor_id):
    supervisor = get_object_or_404(Supervisor,
                                   id=supervisor_id)
    return render(request,
                  "supervisor/supervisor_details.html",
                  {"supervisor": supervisor})
