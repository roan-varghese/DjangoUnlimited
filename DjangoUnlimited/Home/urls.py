from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('view_jobs', views.view_jobs, name ='view_jobs'),
    path('job_details/<int:id>', views.job_details, name ='job_details')
]