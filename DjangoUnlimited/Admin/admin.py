from django.contrib import admin
from .models import Admin
from django.urls import path, re_path
from django.shortcuts import render, redirect

"""
class adminAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_admin', self.something),
        ]
        return custom_urls + urls

    def something(self, request):
        return redirect('/')
"""

# Register your models here.
# admin.site.register(Admin, adminAdmin)
admin.site.register(Admin)