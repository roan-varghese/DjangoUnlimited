from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput
from django.contrib.auth.models import User

from .models import Employer
from Home.models import Industry

class companyNameForm(forms.ModelForm):
    companyName = forms.CharField(label='Company Name', required=True)

    class Meta:
        model = Employer
        fields = ('companyName',)

    def save(self, commit=True):
        employer = super(companyNameForm, self).save(commit=False)
        
        if commit:
            employer.save()
        return employer

class InitialEmployerForm(forms.ModelForm):
    
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(InitialEmployerForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def usernameExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            return True
        return False

    def samePasswords(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        
        if p1 != p2:
            return False
        return True
        

class EmployerForm(forms.ModelForm):
    logo = forms.ImageField(label='Logo', required=False)
    company_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
                                                                attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    company_description = forms.CharField(required=False, widget=forms.Textarea)
    #industry = forms.ModelChoiceField(queryset = Industry.objects.all(), required=True)
    phone_number = forms.CharField(required=False, max_length=50, widget=forms.TextInput(
                                                                                attrs={'class': 'form-control-text', 'style': 'resize:none;'}))

    class Meta:
        model = Employer
        exclude = ['user', 'employer_id', 'industry']