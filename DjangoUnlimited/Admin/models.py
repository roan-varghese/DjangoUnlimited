from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Admin(models.Model):
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user')
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=gender_choices)

