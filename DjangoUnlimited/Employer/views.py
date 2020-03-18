from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction

# Create your views here.

from Accounts.views import isValidated
from .models import Employer
from .forms import InitialEmployerForm, EmployerForm, CreateJobForm
from Admin.models import Admin

def signup(request):
    if request.method == 'POST':
        user_form = InitialEmployerForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("employer_register")

            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("employer_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):
                    employer_form = EmployerForm(request.POST, request.FILES)

                    if employer_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            employer = employer_form.save(commit=False)
                            employer.user = user
                            employer.save()
                            return redirect("login")
                    else:
                        messages.info(request, employer_form.errors)
                        return redirect("employer_register")
                else:
                    messages.info(request,'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')
                    return redirect("employer_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("employer_register")
    else:
        user_form = InitialEmployerForm()
        employer_form = EmployerForm()
        args = {'employer_form': employer_form, 'user_form': user_form}
        return render(request, 'Employer_Registration.html', args)


def edit_profile(request):
    employer = Employer.objects.get(user_id=request.user.id)
    if employer is not None:
        if request.method == 'POST':
            form = EmployerForm(request.POST, request.FILES, instance=employer)

            if form.is_valid():
                form.save()
                return redirect('view_employer_profile')
            else:
                messages.info(request, student_form.errors)
                return redirect("edit_employer_profile")
        else:
            form = EmployerForm(instance=employer)
            args = {'employer_form': form}
            return render(request, 'edit_employer_profile.html', args)
    else:
        messages.info(request, 'This employer user does not exist')


def view_profile(request):
    employer = Employer.objects.get(user_id=request.user.id)
    return render(request, 'view_employer_profile.html', {'employer': employer})


def create_job(request):
    #employer = Employer.objects.get(user_id= request.user.id)
    #admin = Admin.objects.get(user_id=request.user.id)
    if Employer.objects.get(user_id= request.user.id):
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                data = form.save(commit = False)
                data.posted_by = request.user
                data.save()
                return redirect('/')
            else:
                messages.info(request, form.errors)
        else:
            form = CreateJobForm()
            return render(request, "Employer_Create_Jobs.html", {'form': form})
    elif Admin.objects.get(user_id=request.user.id):
        if request.method == 'POST':
            jobForm = CreateJobForm(request.POST)
            companyForm = EmployerForm(request.POST, request.FILES )

            if jobForm.is_valid() and companyForm.is_valid():
                data = jobForm.save(commit=False)
                data.posted_by = request.user
                with transaction.atomic():
                    data.save()
                    companyForm.save()
                    return redirect('/')
            else:
                messages.info(request, jobForm.errors)
                messages.info(request, companyForm.errors)
                return redirect('CreateJob')
        else:
            jobForm = CreateJobForm()
            companyForm = EmployerForm()
            args = {'jobForm': jobForm, 'companyForm': companyForm}
            return render(request, "Employer_Create_Jobs.html", args)

