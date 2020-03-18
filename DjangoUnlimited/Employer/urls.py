from django.urls import path
from . import views

urlpatterns = [
    path('edit_employer_profile',views.edit_employer_profile, name='edit_employer_profile')
]