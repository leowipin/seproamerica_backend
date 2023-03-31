from django.contrib import admin
from .models import Equipamiento

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'brand')

admin.site.register(Equipamiento, EquipmentAdmin)
# Register your models here.
