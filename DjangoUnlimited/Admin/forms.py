from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput

from .models import Admin
from ..DjangoUnlimited import settings


class AdminForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta:
        model = Admin
        exclude = ['admin_id']


class AddIndustryForm(forms.ModelForm):
    industry_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs=
                                                                                         {'class': 'form-control-text',
                                                                                          'style': 'resize:none;'}))
