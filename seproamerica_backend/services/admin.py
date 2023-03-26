from django.contrib import admin
from .models import Servicio

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(Servicio, ServiceAdmin)
# Register your models here.
