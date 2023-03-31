from django.urls import path
from .views import ServiceView, ServiceNamesView, ServiceGetView

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('serviceByID/', ServiceGetView.as_view(), name='servicebyid'),
    path('serviceNames/', ServiceNamesView.as_view(), name='servicenames'),
]