from django.urls import path
from .views import FCMTokenView, OrderClientNotificationView, OrderAdminNotificationView, GetClientNotificationView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
    path('orderClientNoti/', OrderClientNotificationView.as_view(), name='orderclientnoti'),
    path('orderAdminNoti/', OrderAdminNotificationView.as_view(), name='orderadminnoti'),
    path('getClientNoti/', GetClientNotificationView.as_view(), name='getclientnoti'),
]