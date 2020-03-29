from django.contrib import admin
from .models import Admin
from django.urls import path, re_path
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django_comments.models import Comment


# Register your models here.
# admin.site.register(Admin)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(Comment)