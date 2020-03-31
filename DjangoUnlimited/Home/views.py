from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from newsapi import NewsApiClient
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib import messages
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY

# Create your views here.

from Employer.models import Employer
from Admin.models import Admin
from Student.models import Student, StudentJobApplication
from Accounts.views import get_user_type
from .models import Job
from .forms import CreateJobForm, EditJobForm, FilterJobForm
from Employer.forms import EmployerForm
from Student.forms import StudentJobApplicationForm


def index(request):
    return render(request, "index.html", get_user_type(request))


@login_required
def view_jobs(request):
    user = get_user_type(request)

    if user['user_type'] == 'employer':
        jobs = Job.objects.filter(posted_by=request.user.id).order_by('-date_posted')
        args = {'jobs': jobs, 'company': user['obj']}
    elif user['user_type'] == 'student' or user['user_type'] == 'admin':
        jobs = Job.objects.all().order_by('-date_posted')
        companies = Employer.objects.all()
        args = {'jobs': jobs, 'companies': companies}
    else:
        return redirect('/')
    return render(request, 'browse_jobs.html', args)


@login_required
def create_job(request):
    try:
        Employer.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.posted_by = request.user
                data.save()

                message = Mail(
                    from_email='info@murdochcareerportal.com',
                    to_emails=['sethshivangi1998@gmail.com'],
                    subject='New Job has been posted',
                    html_content="A new Job has been posted on the Murdoch Career Portal."
                )
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                #   sg.send(message)

                for skill in request.POST.getlist('skills'):
                    data.skills.add(skill)
                return redirect('/')
            else:
                messages.info(request, form.errors)
                return redirect('create_job')
        else:
            form = CreateJobForm()
            args = {'form': form, 'user': 'employer'}
            return render(request, "employer_create_jobs.html", args)
    except Employer.DoesNotExist:
        pass

    try:
        admin = Admin.objects.get(user_id=request.user.id)
        print(admin.user.id)
        if request.method == 'POST':
            jobForm = CreateJobForm(request.POST)
            companyForm = EmployerForm(request.POST, request.FILES)

            if jobForm.is_valid() and companyForm.is_valid():
                with transaction.atomic():
                    company = companyForm.save(commit=False)
                    company.user_id = admin.user.id
                    company.save()
                    job = jobForm.save(commit=False)
                    job.posted_by = request.user
                    job.save()
                    for skill in request.POST.getlist('skills'):
                        job.skills.add(skill)
                    return redirect('/')
            else:
                messages.info(request, jobForm.errors)
                messages.info(request, companyForm.errors)
                return redirect('create_job')
        else:
            jobForm = CreateJobForm()
            companyForm = EmployerForm()
            args = {'jobForm': jobForm, 'companyForm': companyForm, 'user': 'admin'}
            return render(request, "employer_create_jobs.html", args)
    except Admin.DoesNotExist:
        pass


def filter_jobs(request):
    print("HERE")
    if request.method == 'POST':
        print(request.POST.get)
        min_duration = request.POST.get("min_duration")
        # print(min_duration)
        max_duration = request.POST.get("max_duration")
        # print(max_duration)
        location = request.POST.get("location")
        # print(location)
        job_type_id = request.POST.get("job_type_id")
        # print(job_type_id)
        min_salary = request.POST.get("min_salary")
        # print(min_salary)
        max_salary = request.POST.get("max_salary")
        # print(max_salary)
        industry_id = request.POST.get("industry_id")
        # print(industry_id)
        if min_duration:
            min_duration_jobs = Job.objects.filter(duration__gte=min_duration)
        else:
            min_duration_jobs = Job.objects.all()

        if max_duration:
            max_duration_jobs = Job.objects.filter(duration__lte=max_duration)
        else:
            max_duration_jobs = Job.objects.all()

        if location:
            location_jobs = Job.objects.filter(location=location)
        else:
            location_jobs = Job.objects.all()

        if min_salary:
            min_salary_jobs = Job.objects.filter(salary__gte=min_salary)
        else:
            min_salary_jobs = Job.objects.all()

        if max_salary:
            max_salary_jobs = Job.objects.filter(salary__lte=max_salary)
        else:
            max_salary_jobs = Job.objects.all()

        if job_type_id:
            job_type_id_jobs = Job.objects.filter(job_type_id=job_type_id)
        else:
            job_type_id_jobs = Job.objects.all()

        if industry_id:
            industry_id_jobs = Job.objects.filter(industry_id=industry_id)
        else:
            industry_id_jobs = Job.objects.all()

        filtered_jobs = min_duration_jobs & max_duration_jobs & location_jobs & max_salary_jobs & min_salary_jobs & job_type_id_jobs & industry_id_jobs
        jobs_all = Job.objects.all()
        jobs = jobs_all & filtered_jobs
        print("jobs", jobs)
        args = {'jobs': jobs}
        return render(request, "filtered_jobs.html", args)
    else:
        form = FilterJobForm()
        args = {'form': form}
        return render(request, "filter_jobs.html", args)


@login_required
def job_details(request, id):
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()
    args = {'job': job, 'user': get_user_type(request), 'companies': companies}
    form = StudentJobApplicationForm()
    if request.method == 'POST':
        if request.POST.get("apply"):
            post = form.save(commit=False)
            post.job_id = job
            id = request.user.id
            student = Student.objects.get(user_id=id)
            post.applied = student
            post.date_applied = timezone.now()
            post.save()
            return render(request, 'job_details.html', args)
        elif request.POST.get("viewcandidates"):
            candidates = StudentJobApplication.objects.filter(job_id=job)
            print(candidates)
            args = {'candidates': candidates}
            return render(request, 'view_candidates.html', args)
    return render(request, 'job_details.html', args)


@login_required
def edit_job(request, id):
    job = Job.objects.get(id=id)
    try:
        Employer.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = EditJobForm(request.POST, instance=job)
            if form.is_valid():
                data = form.save(commit=False)
                data.posted_by = request.user
                data.save()
                next = request.POST.get('next', '/')
                return redirect(next)
            else:
                messages.info(request, form.errors)
                return redirect('edit_job')
        else:
            jobForm = EditJobForm()
            args = {'job': job, 'jobForm': jobForm, 'user': 'employer'}
            return render(request, 'edit_job.html', args)
    except Employer.DoesNotExist:
        pass

    try:
        admin = Admin.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            jobForm = CreateJobForm(request.POST, instance=job)
            companyForm = EmployerForm(request.POST, request.FILES, instance=admin)

            if jobForm.is_valid() and companyForm.is_valid():
                with transaction.atomic():
                    company = companyForm.save(commit=False)
                    company.user_id = admin.user.id
                    company.save()
                    job = jobForm.save(commit=False)
                    job.posted_by = request.user
                    job.save()
                    next = request.POST.get('next', '/')
                    return redirect(next)
            else:
                messages.info(request, jobForm.errors)
                messages.info(request, companyForm.errors)
                return redirect('edit_job')
        else:
            jobForm = EditJobForm()
            companyForm = EmployerForm()
            args = {'jobForm': jobForm, 'companyForm': companyForm, 'user': 'admin'}
            return render(request, 'edit_job.html', args)
    except Admin.DoesNotExist:
        pass


@login_required
def my_applications(request):
    id_student = request.user.id
    student = Student.objects.get(user_id=id_student)
    jobs_applied = StudentJobApplication.objects.filter(applied_id=student)
    args = {'jobs_applied': jobs_applied}
    return render(request, 'my_applications.html', args)


@login_required
def news(request):
    # news API to show the latest news
    newsapi = NewsApiClient(api_key='1aab8f2e782a4a588fc28a3292a57979')
    top = newsapi.get_top_headlines(sources='cnn')

    l = top['articles']
    desc = []
    news = []
    img = []
    urllink = []

    for i in range(len(l)):
        f = l[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        urllink.append(f['url'])

    mylist = list(zip(news, desc, img, urllink))

    paginator = Paginator(mylist, 5)

    page = request.GET.get('page')
    mylist = paginator.get_page(page)

    args = {'mylist': mylist}

    return render(request, 'news.html', args)
