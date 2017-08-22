from django import forms
from .models import *

class RegisterForm(forms.Form):
    entity_name=forms.CharField(label="Workspace Name", widget = forms.TextInput(attrs = {"class":"form-control input-md"}))
    maxsize=forms.CharField(label="Max No. of spots", widget = forms.TextInput(attrs = {"class":"form-control input-md"}))
    location_long=forms.CharField(label="Location longitude", widget = forms.TextInput(attrs = {"class":"form-control input-md"}))
    location_lat = forms.CharField(label="Location latitude", widget=forms.TextInput(attrs={"class": "form-control input-md"}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={"class": "form-control input-md"}))

    def clean(self):
        cleaned_data=super(RegisterForm,self).clean()
        return cleaned_data


class ServiceForm(forms.Form):
    name=forms.CharField(label="Service Name", widget = forms.TextInput(attrs = {"class":"form-control input-md"}))
    def clean(self):
        cleaned_data=super(ServiceForm,self).clean()
        return cleaned_data
