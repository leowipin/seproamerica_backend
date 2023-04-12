from django.contrib import admin
from .models import Servicio, ServicioTipoEquipamiento, Pedido, PedidoPersonal, PedidoEquipamiento

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ServiceEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id','equipment_type')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','client', 'service', 'duration', 'total')

class OrderStaffAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'staff')

class OrderEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'equipment_type')

admin.site.register(Servicio, ServiceAdmin)
admin.site.register(ServicioTipoEquipamiento, ServiceEquipmentAdmin)
admin.site.register(Pedido, OrderAdmin)
admin.site.register(PedidoPersonal, OrderStaffAdmin)
admin.site.register(PedidoEquipamiento, OrderEquipmentAdmin)
