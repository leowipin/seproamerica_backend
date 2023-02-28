from django.contrib import admin
from .models import Cargo, Sucursal

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

admin.site.register(Cargo, ChargeAdmin)
admin.site.register(Sucursal, BranchAdmin)
