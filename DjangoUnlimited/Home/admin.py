from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect

from .models import Industry, Skill, Job, JobType

class JobAdmin(admin.ModelAdmin):
    list_display = ('posted_by', 'job_title', 'description', 'salary')
    # change_form_template = "admin/job_change_form.html"
    change_list_template = "admin/job_change_list.html"


# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(Industry)
admin.site.register(Skill)