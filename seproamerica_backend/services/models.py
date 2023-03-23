from django.db import models
from django.contrib.auth import get_user_model
from equipment.models import Equipamiento
from users.models import Cargo

User = get_user_model()

class Servicio(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField()
    set_price = models.BooleanField(default=False)

class ServicioTipoPersonal(models.Model):
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    staff = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    is_optional = models.BooleanField()
    staff_price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    staff_base_hours = models.IntegerField()

class ServicioTipoEquipamiento(models.Model):
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    EQUIPMENT_TYPES = (
        ('móbil', 'móbil'),
        ('vehículo', 'vehículo'),
        ('armamento', 'armamento'),
        ('candado', 'candado'),
    )
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    vehicle_is_optional = models.BooleanField()
    lock_is_optional = models.BooleanField()
    price_range1 = models.DecimalField(max_digits=10, decimal_places=2)
    price_range2 = models.DecimalField(max_digits=10, decimal_places=2)
    price_range3 = models.DecimalField(max_digits=10, decimal_places=2)
    upper_limit1 = models.IntegerField()
    lower_limit1 = models.IntegerField()
    upper_limit2 = models.IntegerField()
    lower_limit2 = models.IntegerField()
    upper_limit3 = models.IntegerField()
    lower_limit3 = models.IntegerField()
    lock_price = models.DecimalField(max_digits=10, decimal_places=2)