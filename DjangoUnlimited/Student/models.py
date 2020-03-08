from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.
from Home.models import Skill, Job


class Student(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user') #this has to be the murdoch student id, not user id
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    DOB = models.DateField()
    personal_email = models.CharField(max_length=100)
    alumni_status = models.BooleanField(default=False)
    expected_graduation_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    # cv field needs to be added


class StudentSkill (models.Model):
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_user_skill')
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skill')


class StudentJobApplication(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='student_job')
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_user_application')