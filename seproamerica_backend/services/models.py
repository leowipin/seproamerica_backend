from django.db import models
from django.contrib.auth import get_user_model
from equipment.models import Equipamiento

"""
User = get_user_model()

class Servicio(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

class ServicioEquipamiento(models.Model):
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'servicio_equipamiento'
"""