from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput

from .models import Student
from ..DjangoUnlimited import settings


class StudentForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    DOB = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True, widget=forms.DateInput(attrs={
        'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY', 'autocomplete': 'off'
    }))
    joining_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True,
                                   widget=forms.DateInput(attrs={
                                       'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                                       'autocomplete': 'off'
                                   }))
    expected_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                               widget=forms.DateInput(attrs={
                                                   'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                                                   'autocomplete': 'off'
                                               }))
    personal_email = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta:
        model = Student
        exclude = ['student_id', 'alumni_status']
