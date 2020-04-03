from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create your views here.

from Accounts.views import isValidated
from .models import Employer
from .forms import InitialEmployerForm, EmployerForm
from Admin.models import Admin
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY

import os
import csv


def signup(request):
    if request.method == 'POST':
        user_form = InitialEmployerForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("employer_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("employer_register")

            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("employer_register")

            elif not user_form.emailDomainExists():
                messages.info(request, 'Email domain does not exist. Try again.')
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

                            message = Mail(
                                from_email='info@murdochcareerportal.com',
                                to_emails=['sethshivangi1998@gmail.com'],
                                subject='New User has signed up',
                                html_content="A new Employer has registered to use the Murdoch Career Portal."
                            )
                            sg = SendGridAPIClient(SENDGRID_API_KEY)
                        #  sg.send(message)

                        return redirect("log_in")
                    else:
                        messages.info(request, employer_form.errors)
                        return redirect("employer_register")
                else:
                    messages.info(request,
                                  'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character.')
                    return redirect("employer_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("employer_register")
    else:
        user_form = InitialEmployerForm()
        employer_form = EmployerForm()
        args = {'employer_form': employer_form, 'user_form': user_form}
        return render(request, 'employer_registration.html', args)


@login_required
def edit_profile(request):
    employer = Employer.objects.get(user_id=request.user.id)
    if employer is not None:
        if request.method == 'POST':
            form = EmployerForm(request.POST, request.FILES, instance=employer)

            if form.is_valid():
                form.save()
                return redirect('view_employer_profile')
            else:
                messages.info(request, form.errors)
                return redirect("edit_employer_profile")
        else:
            form = EmployerForm(instance=employer)
            args = {'employer_form': form, 'employer': employer}
            return render(request, 'edit_employer_profile.html', args)
    else:
        messages.info(request, 'This employer user does not exist')


@login_required
def view_profile(request):
    employer = Employer.objects.get(user_id=request.user.id)
    return render(request, 'view_employer_profile.html', {'employer': employer})


def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    employers = Employer.objects.all()
    writer = csv.writer(response)
    writer.writerow(['1002', 'Amit', 'Mukharji', 'LA', '"Testing"'])
    for employer in employers:
        writer.writerow([employer.company_name, employer.company_description, employer.phone_number])
    return response
