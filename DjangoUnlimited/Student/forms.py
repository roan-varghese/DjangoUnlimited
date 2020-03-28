from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import models
from datetime import date

from .models import Student, StudentJobApplication
from Home.models import Skill
from DjangoUnlimited import settings

# Note: we need dnspython for this to work
import dns.resolver, dns.exception


class InitialStudentForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(InitialStudentForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def usernameExists(self):
        studentID = self.cleaned_data.get("email")
        if User.objects.filter(username=studentID).exists():
            return True
        return False

    def emailExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            return True
        return False

    def emailDomainExists(self):
        email = self.cleaned_data.get("email")
        domain = email.split('@')[1]
        try:
            dns.resolver.query(domain, 'MX')
            return True

        except dns.exception.DNSException:
            return False

    def samePasswords(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            return False
        return True


class StudentForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
    DOB = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True, label='Date of Birth',
                          widget=forms.DateInput(attrs={
                              'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                              'autocomplete': 'off'
                          }))
    student_id = forms.CharField(label='Student ID')
    alumni_status = forms.BooleanField(required=False, label='Select if you are a Murdoch University Alumni',
                                       widget=forms.CheckboxInput(attrs={'onClick': 'disable_fields(this.checked)'}))
    expected_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                               label='Expected Graduation Date',
                                               widget=forms.DateInput(attrs={
                                                   'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                                                   'autocomplete': 'off'
                                               }))
    personal_email = forms.EmailField(required=False, label='Personal Email Address')
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)
    dp = forms.ImageField(label='Select a profile picture', required=False)
    cv = forms.FileField(allow_empty_file=False, label='Attach CV')

    class Meta:
        model = Student
        exclude = ['user', 'jobs_applied']


class EditStudentProfileInitialForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )
        labels = (
            {'first_name': 'First Name'},
            {'last_name': 'Last Name'}
        )
        exclude = ['email', 'password1', 'password2']

class EditStudentProfileForm(forms.ModelForm):
    gender_choices = [
            ('Male', 'Male'),
            ('Female', 'Female')
        ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
    DOB = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True, label='Date of Birth',
                          widget=forms.DateInput(attrs={
                              'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                              'autocomplete': 'off'
                          }))
    alumni_status = forms.BooleanField(required=False, label='Select if you are a Murdoch University Alumni',
                                       widget=forms.CheckboxInput(attrs={'onClick': 'disable_fields(this.checked)'}))
    expected_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                               label='Expected Graduation Date',
                                               widget=forms.DateInput(attrs={
                                                   'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
                                                   'autocomplete': 'off'
                                               }))
    personal_email = forms.EmailField(required=False, label='Personal Email Address')
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)
    dp = forms.ImageField(label='Select a profile picture', required=False)
    cv = forms.FileField(allow_empty_file=False, label='Attach CV')

    class Meta:
        model = Student
        exclude = ['user', 'jobs_applied', 'student_id']


class StudentJobApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentJobApplication

        fields = ['job_id', 'applied']


"""
class StudentSkillsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('skills', )
        widgets = {
            'skills': forms.CheckboxSelectMultiple
        }
        exclude = ['student_id', 'alumni_status']
"""
