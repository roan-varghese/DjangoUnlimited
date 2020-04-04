from django.urls import path, include
from . import views

urlpatterns = [
    path('create_admin', views.create_admin, name='admin_register'),
    path('edit_admin_profile', views.edit_profile, name='edit_admin_profile'),
    path('view_admin_profile', views.view_profile, name='view_admin_profile'),
    path('admin_create_job', views.create_job, name='admin_create_job'),
]
