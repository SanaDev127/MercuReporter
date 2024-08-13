from django import forms
from accounts.models import CustomUser, Supervisor
from transactions.models import Brand
from django.core.validators import FileExtensionValidator


class CreateFleetForm(forms.Form):
    name = forms.CharField()


class AddSupervisorForm(forms.ModelForm):
    password = forms.CharField(label='Supervisor Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class OwnerAddVehicleForm(forms.Form):

    registration_number = forms.CharField(label="Vehicle Registration Number")
    model_description = forms.CharField(label="Vehicle Model Description")
    addedBy = forms.ModelChoiceField(queryset=Supervisor.supervisors.get_queryset(), label="Vehicle Supervisor")


class SupervisorAddVehicleForm(forms.Form):
    registration_number = forms.CharField(label="Vehicle Registration Number")
    model_description = forms.CharField(label="Vehicle Model Description")


class AddMerchantForm(forms.Form):
    Name = forms.CharField(label="Merchant Name")
    # Probably going to change this when I know how to pick location off a map
    address = forms.CharField(label="Fuel Station Address", required=False)
    latitude = forms.CharField(label="Fuel Station Latitude", required=False)
    longitude = forms.CharField(label="Fuel Station Longitude", required=False)
    brand = forms.ModelChoiceField(queryset=Brand.brands.get_queryset(), label="Brand the merchant belongs to")


class AddBrandForm(forms.Form):
    Name = forms.CharField(label="Brand Name")


class UploadVehicleFileForm(forms.Form):
    file = forms.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['xlsx'])
    ])
