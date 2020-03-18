from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.login, name='log_in'),
    path('ForgotPassword', views.forgot_password, name='forgot_password'),

    path('EmployerRegistration', views.employer_signup, name='employer_register'),

    path('logout', views.logout, name='logout'),
    # path('confirm_logout', views.confirm_logout, name='logout'),
    # path('cancel_logout', views.cancel_logout, name='logout')

    path('', include('django.contrib.auth.urls')),
    path(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(), 
        name='password_reset'
    ),
    path(
        r'^password_reset_done/$', 
        auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_link_sent.html'),
        name='password_reset_done'
    ),
    # path(
    #     r'^password_reset_confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$',
    #     auth_views.PasswordResetConfirmView,
    #     name='password_reset_confirm'
    # )
]