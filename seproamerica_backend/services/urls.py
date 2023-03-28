from django.urls import path
from .views import ServiceView, ServiceNamesView

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('serviceNames/', ServiceNamesView.as_view(), name='servicenames'),
]