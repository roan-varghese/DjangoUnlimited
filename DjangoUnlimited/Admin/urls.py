from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^create_admin/$', views.createAdmin, name='admin_register'),
]
