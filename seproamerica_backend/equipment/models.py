from django.db import models
from users.models import Sucursal
"""
class Equipamiento(models.Model):
    EQUIPMENT_TYPES = (
        ('móbil', 'móbil'),
        ('vehículo', 'vehículo'),
        ('armamento', 'armamento'),
        ('candado', 'candado'),
    )
    type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    branch = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
"""