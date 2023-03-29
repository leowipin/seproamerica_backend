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
    staff_is_optional = models.BooleanField()
    staff_number_is_optional = models.BooleanField()
    staff_price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    staff_base_hours = models.IntegerField(null=True)

class ServicioTipoEquipamiento(models.Model):
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    EQUIPMENT_TYPES = (
        ('móbil', 'móbil'),
        ('vehículo', 'vehículo'),
        ('armamento', 'armamento'),
        ('candado', 'candado'),
    )
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES, null=True)
    equipment_is_optional = models.BooleanField()
    equipment_number_is_optional = models.BooleanField()
    equipment_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_range1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_range2 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_range3 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    upper_limit1 = models.IntegerField(null=True)
    lower_limit1 = models.IntegerField(null=True)
    upper_limit2 = models.IntegerField(null=True)
    lower_limit2 = models.IntegerField(null=True)
    upper_limit3 = models.IntegerField(null=True)
    lower_limit3 = models.IntegerField(null=True)