from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('ForgotPassword', views.forgot_password, name='forgot_password'),

    path('Registration', views.student_signup, name='register'),
    path('EmployerRegistration', views.employer_signup, name='employer_register'),

    path('logout', views.logout, name='logout'),
    # path('confirm_logout', views.confirm_logout, name='logout'),
    # path('cancel_logout', views.cancel_logout, name='logout')
]