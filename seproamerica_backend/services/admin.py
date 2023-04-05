from django.contrib import admin
from .models import Servicio, ServicioTipoEquipamiento

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ServiceEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id','equipment_type')

admin.site.register(Servicio, ServiceAdmin)
admin.site.register(ServicioTipoEquipamiento, ServiceEquipmentAdmin)
# Register your models here.
