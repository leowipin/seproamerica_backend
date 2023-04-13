from django.urls import path
from .views import ServiceView, ServiceNamesView, ServiceGetView, OrderClientView, OrderClientNamesView

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('serviceByID/', ServiceGetView.as_view(), name='servicebyid'),
    path('serviceNames/', ServiceNamesView.as_view(), name='servicenames'),
    path('orderClient/', OrderClientView.as_view(), name='orderclient'),
    path('orderClientNames/', OrderClientNamesView.as_view(), name='orderclientnames'),
]