from django.contrib import admin
from .models import Cargo, Sucursal, Usuario, GroupType, TokenFCM

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','email')

class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type')

class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'created_at')

admin.site.register(Cargo, ChargeAdmin)
admin.site.register(Sucursal, BranchAdmin)
admin.site.register(Usuario, UserAdmin)
admin.site.register(GroupType, GroupTypeAdmin)
admin.site.register(TokenFCM, FCMTokenAdmin)
