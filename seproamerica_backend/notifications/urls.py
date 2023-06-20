from django.urls import path
from .views import FCMTokenView, OrderClientNotificationView, OrderAdminNotificationView, ClientNotificationsView, AdminNotificationsView, AdminNotificationDeleteView, ClientNotificationDeleteView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
    path('orderClientNoti/', OrderClientNotificationView.as_view(), name='orderclientnoti'),
    path('orderAdminNoti/', OrderAdminNotificationView.as_view(), name='orderadminnoti'),
    path('clientNoti/', ClientNotificationsView.as_view(), name='clientnoti'),
    path('clientNotiDelete/', ClientNotificationDeleteView.as_view(), name='clientnotidelete'),
    path('adminNoti/', AdminNotificationsView.as_view(), name='adminnoti'),
    path('adminNotiDelete/', AdminNotificationDeleteView.as_view(), name='adminnotidelete'),
]