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
from .models import Job, Skill
from .forms import CreateJobForm, EditJobForm, FilterJobForm, FilterStudentForm
from Employer.forms import EmployerForm
from Student.forms import StudentJobApplicationForm


def index(request):
    return render(request, "index.html", get_user_type(request))


@login_required
def view_jobs(request):
    user = get_user_type(request)
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
        form = FilterJobForm()
        print("user", get_user_type(request))
        args = {'jobs': jobs, 'user': get_user_type(request), 'form': form}
        return render(request, "browse_jobs.html", args)
    elif user['user_type'] == 'employer':
        jobs = Job.objects.filter(posted_by=request.user.id).order_by('-date_posted')
        args = {'jobs': jobs, 'company': user['obj']}
    elif user['user_type'] == 'student' or user['user_type'] == 'admin':
        jobs = Job.objects.all().order_by('-date_posted')
        companies = Employer.objects.all()
        form = FilterJobForm()
        args = {'jobs': jobs, 'companies': companies, 'form': form, 'user_type': user}
    else:
       redirect('/')
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

    return redirect('log_in')


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
            form = EditJobForm(request.POST, request.FILES, instance=job)
            if form.is_valid():
                data = form.save(commit=False)
                data.posted_by = request.user
                data.save()
                next = request.POST.get('next', '/')
                return redirect(next)
            else:
                messages.info(request, form.errors)
                return redirect(request.path_info)
        else:
            jobForm = EditJobForm(instance=job)
            args = {'job': job, 'jobForm': jobForm, 'user': 'employer'}
            return render(request, 'edit_job.html', args)
    except Employer.DoesNotExist:
        pass

    try:
        admin = Admin.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            jobForm = EditJobForm(request.POST, instance=job)
            companyForm = EmployerForm(request.POST, request.FILES, instance=admin)

            if jobForm.is_valid() and companyForm.is_valid():
                with transaction.atomic():
                    company = companyForm.save(commit=False)
                    company.user_id = admin.user.id
                    company.save()
                    job = jobForm.save(commit=False)
                    job.posted_by = request.user
                    job.save()
                    next_page = request.POST.get('next', '/')
                    return redirect(next_page)
            else:
                messages.info(request, jobForm.errors)
                messages.info(request, companyForm.errors)
                return redirect(request.path_info)
        else:
            jobForm = EditJobForm()
            companyForm = EmployerForm()
            args = {'jobForm': jobForm, 'companyForm': companyForm, 'user': 'admin'}
            return render(request, 'edit_job.html', args)
    except Admin.DoesNotExist:
        pass

    return redirect('log_in')
    
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

    args = {'mylist': mylist, 'user': get_user_type(request)}

    return render(request, 'news.html', args)


@login_required
def delete_job(request, id):
    job = Job.objects.get(id=id)
    if request.method == 'POST':
        job.status = 'Deleted'
        job.save()
        messages.success(request, "You have successfully deleted the job")
        args = {'job': job}
        return render(request, 'delete_job.html', args)
    else:
        form = EditJobForm()
        args = {'job': job, 'form': form}
        return render(request, 'delete_job.html', args)


@login_required
def close_job(request, id):
    job = Job.objects.get(id=id)
    if request.method == 'POST':
        job.status = 'Closed'
        job.date_closed = timezone.now()
        job.save()
        messages.success(request, "You have successfully closed the job")
        args = {'job': job}
        return render(request, 'close_job.html', args)
    else:
        form = EditJobForm()
        args = {'job': job, 'form': form}
        return render(request, 'close_job.html', args)


@login_required
def view_students(request):
    user = get_user_type(request)
    if request.method == 'POST':
        alumni_status = request.POST.get("alumni_status")
        #print(alumni_status)
        skills = request.POST.get("skills")
        #print(skills)
        min_graduation_date = request.POST.get('min_graduation_date')
        #print(min_graduation_date)
        max_graduation_date = request.POST.get('max_graduation_date')
        #print(max_graduation_date)

        if alumni_status:
            alumni_status_students = Student.objects.filter(alumni_status=True)
        else:
            alumni_status_students = Student.objects.all()

        if skills:
            skills_students = Student.objects.filter(skills=skills)
        else:
            skills_students = Student.objects.all()

        if min_graduation_date:
            min_graduation_date_students = Student.objects.filter(expected_graduation_date__gte=min_graduation_date)
        else:
            min_graduation_date_students = Student.objects.all()

        if max_graduation_date:
            max_graduation_date_students = Student.objects.filter(expected_graduation_date__lte=max_graduation_date)
        else:
            max_graduation_date_students = Student.objects.all()

        filtered_stds = skills_students & alumni_status_students & min_graduation_date_students & max_graduation_date_students
        students_all = Student.objects.all()
        students = students_all & filtered_stds
        form = FilterStudentForm()
        print("students", students)
        args = {'students': students, 'form': form, 'user': user}
        return render(request, "browse_students.html", args)
    elif user['user_type'] == 'employer' or user['user_type'] == 'admin':
        students = Student.objects.all()
        users = User.objects.all()
        form = FilterStudentForm()
        args = {'students': students, 'users': users, 'form': form}
    else:
        return redirect('/')
    return render(request, 'browse_students.html', args)


@login_required
def student_details(request, id):
    student = Student.objects.get(user_id=id)
    args = {'student': student, 'user': get_user_type(request)}
    return render(request, 'student_details.html', args)
