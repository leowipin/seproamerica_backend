from django.urls import path
from .views import FCMTokenView, OrderClientNotificationView, OrderAdminNotificationView, GetClientNotificationsView, GetSpecificNotificationView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
    path('orderClientNoti/', OrderClientNotificationView.as_view(), name='orderclientnoti'),
    path('orderAdminNoti/', OrderAdminNotificationView.as_view(), name='orderadminnoti'),
    path('getClientNoti/', GetClientNotificationsView.as_view(), name='getclientnotis'),
    path('getSpecificClientNoti/', GetSpecificNotificationView.as_view(), name='getclientspecificnoti'),
]