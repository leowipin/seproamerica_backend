from django.urls import path
from .views import FCMTokenView, OrderClientNotificationView, OrderAdminNotificationView, ClientNotificationsView, GetSpecificNotificationView

urlpatterns = [
    path('fcmToken/', FCMTokenView.as_view(), name='fcmtoken'),
    path('orderClientNoti/', OrderClientNotificationView.as_view(), name='orderclientnoti'),
    path('orderAdminNoti/', OrderAdminNotificationView.as_view(), name='orderadminnoti'),
    path('clientNoti/', ClientNotificationsView.as_view(), name='clientnoti'),
    path('getSpecificClientNoti/', GetSpecificNotificationView.as_view(), name='getclientspecificnoti'),#no usado
]