from django.shortcuts import render, redirect
from Employer.models import Employer
from Student.models import Student, StudentJobApplication
from Accounts.views import get_user_type
from django.views.generic import TemplateView
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Job
from django.utils import timezone
from Student.forms import StudentJobApplicationForm
from newsapi import NewsApiClient
from django.core.cache import cache
from django.core.paginator import Paginator


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
        jobs = Job.objects.filter(posted_by=request.user.id).order_by('-date_posted')
        args = {'jobs': jobs, 'company': user['obj']}
    elif user['user_type'] == 'student':
        jobs = Job.objects.all().order_by('-date_posted')
        companies = Employer.objects.all()
        args = {'jobs': jobs, 'companies': companies}
    else:
        return redirect('/')
    return render(request, 'browse_jobs.html', args)


def job_details(request, id):
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()
    args = {'job': job, 'user': get_user_type(request), 'companies': companies}
    form = StudentJobApplicationForm()
    if request.method == 'POST':
        print('HI')
        if request.POST.get("apply"):
            print('HELLO123')
            post = form.save(commit=False)
            post.job_id = job
            id = request.user.id
            student = Student.objects.get(user_id=id)
            post.applied = student
            post.date_applied = timezone.now()
            post.save()
            return render(request, 'job_details.html', args)
        elif request.POST.get("viewcandidates"):
            print('HELLO111')
            candidates = StudentJobApplication.objects.filter(job_id=job)
            print(candidates)
            args = {'candidates': candidates}
            return render(request, 'view_candidates.html', args)
    return render(request, 'job_details.html', args)


def my_applications(request):
    id_student = request.user.id
    student = Student.objects.get(user_id=id_student)
    jobs_applied = StudentJobApplication.objects.filter(applied_id=student)
    args = {'jobs_applied': jobs_applied}
    return render(request, 'my_applications.html', args)


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
