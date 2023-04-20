from django.contrib import admin
from .models import Cardauth

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'token')

admin.site.register(Cardauth, CardAdmin)
# Register your models here.
