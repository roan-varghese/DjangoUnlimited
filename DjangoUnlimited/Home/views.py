from django.shortcuts import render, redirect
from Employer.models import Employer
from Student.models import Student
from Accounts.views import get_user_type
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Job

# Create your views here.

def index(request):
    return render(request, "index.html", get_user_type(request))
    
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
        return render(request, 'index.html')


def view_jobs(request):
    user = get_user_type(request)

    if user['user_type'] == 'employer' or user['user_type'] == 'admin':
        jobs = Job.objects.filter(posted_by=request.user.id).order_by('date_posted')
        args = {'jobs': jobs, 'company': user['obj']}
    elif user['user_type'] == 'student':
        jobs = Job.objects.all().order_by('date_posted')
        companies = Employer.objects.all()
        args = {'jobs': jobs,'companies': companies }
    else:
        return redirect('/')
    return render(request, 'browse_jobs.html', args)


def job_details(request, id):
    job = Job.objects.get(id = id)
    companies = Employer.objects.all()
    args = {'job': job, 'user': get_user_type(request), 'companies': companies}
    return render(request, 'job_details.html', args)
