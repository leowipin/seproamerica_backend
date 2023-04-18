from django.contrib import admin
from .models import Servicio, ServicioTipoEquipamiento, Pedido, PedidoPersonal, PedidoEquipamiento, EquipamientoAsignado, PersonalAsignado

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

class OrderStaffAssignedAdmin(admin.ModelAdmin):
    list_display = ('id', 'operational_staff', 'order')    

class OrderEquipmentAssignedAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'order')

admin.site.register(Servicio, ServiceAdmin)
admin.site.register(ServicioTipoEquipamiento, ServiceEquipmentAdmin)
admin.site.register(Pedido, OrderAdmin)
admin.site.register(PedidoPersonal, OrderStaffAdmin)
admin.site.register(PedidoEquipamiento, OrderEquipmentAdmin)
admin.site.register(PersonalAsignado, OrderStaffAssignedAdmin)
admin.site.register(EquipamientoAsignado, OrderEquipmentAssignedAdmin)
