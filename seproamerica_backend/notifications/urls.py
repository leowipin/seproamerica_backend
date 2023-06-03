from django.urls import path
from .views import FCMTokenView, OrderClientNotificationView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
    path('orderClientNoti/', OrderClientNotificationView.as_view(), name='orderClientNoti'),
]