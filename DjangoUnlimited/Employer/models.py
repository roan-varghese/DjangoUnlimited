from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from Home.models import Industry


class Employer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # employer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_user')
    company_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    # industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry')


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employer.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employer.save()
