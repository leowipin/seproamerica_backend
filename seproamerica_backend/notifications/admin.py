from django.contrib import admin
from .models import TokenFCM, OrderAdminNotification, OrderClientNotification
# Register your models here.

class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'created_at')

class OrderAdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'message', 'order', 'date_sended')

class OrderClientNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'message', 'user', 'date_sended')

admin.site.register(TokenFCM, FCMTokenAdmin)
admin.site.register(OrderAdminNotification, OrderAdminNotificationAdmin)
admin.site.register(OrderClientNotification, OrderClientNotificationAdmin)