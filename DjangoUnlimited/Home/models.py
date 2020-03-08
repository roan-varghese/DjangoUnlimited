from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
from Admin.models import Admin

class Industry(models.Model):
    industry_name = models.CharField(max_length=50)


class Skill(models.Model):
    skill_name = models.CharField(max_length=50)


class JobSkill(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skill_for_job')
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='job_skill')


class JobType(models.Model):
    type_name = models.CharField(max_length=50)


class Job(models.Model):
    industry_id = models.ForeignKey(Industry, on_delete = models.CASCADE, related_name ='job_industry')
    duration = models.IntegerField()
    date_posted = models.DateField(null=False, blank=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_author')
    job_title =  models.CharField(max_length=100)
    desc = models.TextField()
    job_status = [
        ('Open','Open'),
        ('Closed','Closed'),
        ('Deleted','Deleted')
    ]
    date_closed = models.DateFirl(null=True, blank=True)
    location = models.CharField(max_length=100)
    job_type_id = models.ForeignKey(JobType, on_delete = models.CASCADE, related_name ='job_type')
    salary = models.FloatField()


class HelpDeskComplaints(models.Model):
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainant')
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    details = models.TextField()
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='assigned_admin')