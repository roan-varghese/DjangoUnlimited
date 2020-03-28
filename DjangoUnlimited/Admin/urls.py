from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^create_admin/$', views.create_admin, name='admin_register'),
    re_path(r'edit_admin_profile/$', views.edit_profile, name='edit_admin_profile'),
    re_path(r'^view_admin_profile/$', views.view_profile, name='view_admin_profile'),
]
