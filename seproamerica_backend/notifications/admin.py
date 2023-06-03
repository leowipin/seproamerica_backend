from django.contrib import admin
from .models import TokenFCM, OrderAdminNotification
# Register your models here.

class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'created_at')

class OrderAndminNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'message', 'order')

admin.site.register(TokenFCM, FCMTokenAdmin)
admin.site.register(OrderAdminNotification, OrderAndminNotificationAdmin)