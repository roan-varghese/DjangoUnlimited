from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput

from .models import Employer
from ..DjangoUnlimited import settings


class EmployerForm(forms.ModelForm):

    company_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    phone_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))

    class Meta:
        model = Employer
        exclude = ['employer_id', 'industry']

