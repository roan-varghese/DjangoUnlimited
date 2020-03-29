from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY

# Create your views here.

from Accounts.views import isValidated
from .models import Student
from .forms import *


def student_signup(request):
    if request.method == 'POST':
        user_form = InitialStudentForm(request.POST)
        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("student_registration")
            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("student_registration")
            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("student_registration")
            elif not user_form.emailDomainExists():
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("student_registration")
            else:
                if isValidated(user_form.cleaned_data.get('password1')):
                    student_form = StudentForm(request.POST, request.FILES)
                    if student_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            student = student_form.save(commit=False)
                            student.user = user
                            student.save()
                            for skill in request.POST.getlist('skills'):
                                student.skills.add(skill)

                            message = Mail(
                                from_email='info@murdochcareerportal.com',
                                to_emails=['sethshivangi1998@gmail.com'],
                                subject='New User has signed up',
                                html_content="A new Student has registered to use the Murdoch Career Portal."
                            )
                            sg = SendGridAPIClient(SENDGRID_API_KEY)
                            sg.send(message)
                            return redirect("log_in")
                    else:
                        messages.info(request, student_form.errors)
                        return redirect("student_registration")
                else:
                    messages.info(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')
                    return redirect("student_registration")
        else:
            messages.info(request, user_form.errors)
            return redirect("student_registration")
    else:
        user_form = InitialStudentForm()
        student_form = StudentForm()
        args = {'student_form': student_form, 'user_form': user_form}

        return render(request, 'student_registration.html', args)


def edit_profile(request):
    student = Student.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditStudentProfileInitialForm(request.POST, instance=request.user)
        student_form = EditStudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
                return redirect('view_student_profile')
        else:
            print(student_form)
            messages.info(request, student_form.errors)
            messages.info(request, user_form.errors)
            return redirect("edit_student_profile")
    else:
        user_form = EditStudentProfileInitialForm(instance=request.user)
        student_form = EditStudentProfileForm(instance=student)
        args = {'student_form': student_form, 'user_form': user_form}
        return render(request, 'edit_student_profile.html', args)

def view_profile(request):
    user = request.user
    student = Student.objects.get(user_id=user.id)
    args = {'student': student, 'user': user}
    return render(request, 'view_student_profile.html', args)