from django.contrib import admin
from .models import Cargo, Sucursal, Usuario

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','email')

admin.site.register(Cargo, ChargeAdmin)
admin.site.register(Sucursal, BranchAdmin)
admin.site.register(Usuario, UserAdmin)
