from django import forms
from django.core.validators import FileExtensionValidator


class UploadTransactionFileForm(forms.Form):
    file = forms.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['xlsx'])
    ])


class ScanTransactionForm(forms.Form):
    file = forms.ImageField()


class FilterTransactionDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget, label="From")
    end_date = forms.DateField(widget=forms.SelectDateWidget, label="To")





    