from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#from Accounts.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='admin_user')
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='admin_user')
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)
    dp = models.ImageField(upload_to='profile_pictures', blank=True)