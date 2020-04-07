from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Industry, Skill, Job, JobType
from Employer.models import Employer
from Student.models import Student

class JobAdmin(admin.ModelAdmin):

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "posted_by":
    #         kwargs["queryset"] = User.objects.filter(
    #                 is_staff__in=['False']
    #             )
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('posted_by', 'job_title', 'description', 'salary')
    change_list_template = "admin/job_change_list.html"


# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(Industry)
admin.site.register(Skill)