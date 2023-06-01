from django.contrib import admin
from .models import TokenFCM
# Register your models here.

class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'created_at')

admin.site.register(TokenFCM, FCMTokenAdmin)