from django import forms
from fleet.models import Fleet


class SelectFleetForm(forms.Form):
    fleet = forms.ModelChoiceField(Fleet.fleets.get_queryset(),
                                   label="Select a fleet",
                                   widget=forms.Select(
                                       attrs={"onchange": "this.form.submit();"}
                                   )
                                   )



