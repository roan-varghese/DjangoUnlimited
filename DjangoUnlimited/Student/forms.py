from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput

from .models import Student
# from ..DjangoUnlimited import settings
from django.contrib.auth.models import User

class initialStudentForm(forms.ModelForm):
    
    studentID = forms.CharField(label='Student ID')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'studentID',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(initialStudentForm, self).save(commit=False)
        user.username = self.cleaned_data["studentID"]
        user.set_password(self.cleaned_data["password1"])
        # user.active = false
        if commit:
            user.save()
        return user

    def usernameExists(self):
        studentID = self.cleaned_data.get("studentID")
        if User.objects.filter(username=studentID).exists():
            print('ok')
            return True
            # raise forms.ValidationError("Username already taken. Try a different one.")
        print('not ok')
        return False

    def samePasswords(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        
        if p1 != p2:
            return False
            # raise forms.ValidationError("Passwords not matching. Try again.")
        return True
        


class StudentForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    # DOB = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True, widget=forms.DateInput(attrs={
    #     'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY', 'autocomplete': 'off'
    # }))
    # joining_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True,
    #                                widget=forms.DateInput(attrs={
    #                                    'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
    #                                    'autocomplete': 'off'
    #                                }))
    # expected_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
    #                                            widget=forms.DateInput(attrs={
    #                                                'class': 'datepicker form-control-text', 'placeholder': 'DD-MM-YYYY',
    #                                                'autocomplete': 'off'
    #                                            }))
    personal_email = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta:
        model = Student
        exclude = ['student_id', 'alumni_status']
