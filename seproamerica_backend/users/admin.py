from django.contrib import admin
from .models import Charge

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

admin.site.register(Charge, ChargeAdmin)
