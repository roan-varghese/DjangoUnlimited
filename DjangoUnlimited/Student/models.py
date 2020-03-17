from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.
from Home.models import Skill, Job

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_user')
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    dp = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    DOB = models.DateField()
    personal_email = models.CharField(max_length=100)
    alumni_status = models.BooleanField(default=False)
    expected_graduation_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    #skills = models.ManyToManyField(Skill, through='StudentSkill')
    jobs_applied = models.ManyToManyField(Job, through='StudentJobApplication')
    cv = models.FileField(upload_to='documents', default='./DefaultCV.txt')

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name

class StudentSkill(models.Model):
    #student_user = str
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_skill')
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skill')
    date_skill_added = models.DateTimeField(auto_now_add=True)


class StudentJobApplication(models.Model):
    #student_user = str
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='student_job')
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_user_application')
    date_applied = models.DateTimeField(auto_now_add=True)