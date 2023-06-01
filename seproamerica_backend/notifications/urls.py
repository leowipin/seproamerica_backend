from django.urls import path
from .views import FCMTokenView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
]