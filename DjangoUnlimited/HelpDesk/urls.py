from django.urls import path

from .views import HelpDeskFormView, HelpDeskRequests, MyHelpDeskRequests

urlpatterns = [
    path('HelpDesk/', HelpDeskFormView.as_view(), name='HelpDesk'),
    path('HelpDesk/<int:pk>', HelpDeskFormView.as_view(), name='HelpDesk'),
    path('HelpDesk/requests', HelpDeskRequests.as_view(), name='HelpDeskRequests'),
    path('HelpDesk/myrequests', MyHelpDeskRequests.as_view(), name='MyHelpDeskRequests'),

]
