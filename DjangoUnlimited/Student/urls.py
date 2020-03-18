from django.urls import path
from . import views

urlpatterns = [
    path('Registration', views.student_signup, name='register'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('view_profile', views.view_profile, name='view_profile'),
]