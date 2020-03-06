from django.db import models

# Create your models here.


class Industry(models.Model):
    industry_name = models.CharField(max_length=50)


class Skill(models.Model):
    skill_name = models.CharField(max_length=50)

