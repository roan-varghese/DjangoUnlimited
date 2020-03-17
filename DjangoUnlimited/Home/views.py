from django.shortcuts import render, redirect
from Employer.models import Employer
from Student.models import Student
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'Index.html')
    
def has_employer(request):
    hasEmployer = False
    try:
        hasEmployer = (request.user.employer is not None)
    except Employer.DoesNotExist:
        pass

    return hasEmployer

def has_student(request):
    hasStudent = False
    try:
        hasStudent = (request.user.student is not None)
    except Student.DoesNotExist:
        pass

    return hasStudent

@login_required
def profile(request):
    if has_employer(request):
        print('has employer')
        return render(request, 'view_employer_profile.html')
    elif has_student(request):
        print('has student')
        return render(request, 'view_student_profile.html')
    else:
        return render(request, 'Index.html')