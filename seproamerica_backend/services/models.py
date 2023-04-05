from django.db import models
from django.contrib.auth import get_user_model
from users.models import Cargo, PersonalOperativo, Cliente, CuentaTelefono
from equipment.models import Equipamiento

User = get_user_model()

class Servicio(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField()
    set_price = models.BooleanField(default=False)
    requires_origin_and_destination = models.BooleanField()

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
        ('candado satelital', 'candado satelital'),
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

class Pedido(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    phone_account = models.ForeignKey(CuentaTelefono, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    origin_latitude = models.FloatField()
    origin_length = models.FloatField()
    destination_latitude = models.FloatField()
    destination_length = models.FloatField()

class PedidoPersonal(models.Model):
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    staff = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    is_required = models.BooleanField()
    staff_number_is_optional = models.BooleanField()
    staff_number = models.IntegerField(null=True, blank=True)

class PedidoEquipamiento(models.Model):
    EQUIPMENT_TYPES = (
        ('móbil', 'móbil'),
        ('vehículo', 'vehículo'),
        ('armamento', 'armamento'),
        ('candado satelital', 'candado satelital'),
    )
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES, null=True)
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    is_required = models.BooleanField()
    equipment_number_is_optional = models.BooleanField()
    equipment_number = models.IntegerField(null=True, blank=True)

class PersonalAsignado(models.Model):
    operational_staff = models.ForeignKey(PersonalOperativo, on_delete=models.CASCADE)
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    is_leader = models.BooleanField()

class EquipamientoAsignado(models.Model):
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)