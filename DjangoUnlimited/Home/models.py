from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
from Admin.models import Admin
from django.db.models import ManyToManyField


class Industry(models.Model):
    industry_name = models.CharField(max_length=50)

    def clean(self):
        self.industry_name = self.industry_name.capitalize()

    def __str__(self):
        name = self.industry_name
        return name


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.skill_name = self.skill_name.capitalize()

    def __str__(self):
        name = self.skill_name
        return name


class JobType(models.Model):
    type_name = models.CharField(max_length=50)

    def clean(self):
        self.type_name = self.type_name.capitalize()

    def __str__(self):
        name = self.type_name
        return name


class Job(models.Model):
    date_posted = models.DateField(null=False, blank=False, auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_author')
    job_title = models.CharField(max_length=100)
    description = models.TextField()
    job_status = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted')
    ]
    status = models.CharField(max_length=15, choices=job_status, default='Open')
    date_closed = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100)
    job_type_id = models.ForeignKey(JobType, on_delete=models.CASCADE, related_name='job_type')
    industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='job_industry')
    duration = models.DurationField(null=True)
    salary = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)])
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        title = self.job_title
        return title


class HelpDeskComplaints(models.Model):
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainant')
    subject = models.CharField(max_length=100)
    details = models.TextField()
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='assigned_admin')

