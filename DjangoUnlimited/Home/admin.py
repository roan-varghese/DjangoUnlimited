from django.contrib import admin
from .models import Industry, Skill, Job, JobType

# Register your models here.
admin.site.register(Industry)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(JobType)