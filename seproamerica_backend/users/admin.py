from django.contrib import admin
from .models import Cargo, Sucursal, Usuario, GroupType, ImagenesPerfil, Empresa

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','email')

class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type')

class UserPictureAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'url_img')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name',)


admin.site.register(Cargo, ChargeAdmin)
admin.site.register(Sucursal, BranchAdmin)
admin.site.register(Usuario, UserAdmin)
admin.site.register(GroupType, GroupTypeAdmin)
admin.site.register(ImagenesPerfil, UserPictureAdmin)
admin.site.register(Empresa, CompanyAdmin)