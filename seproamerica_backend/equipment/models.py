from django.db import models
from users.models import Sucursal
from datetime import date


class Equipamiento(models.Model):
    EQUIPMENT_TYPES = (
        ('móbil', 'móbil'),
        ('vehículo', 'vehículo'),
        ('armamento', 'armamento'),
        ('candado', 'candado'),
    )
    type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    branch = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    


class Telefono(models.Model):
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=20)
    purchase_date = models.DateField()

class Vehiculo(models.Model):
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    plate = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    engine = models.CharField(max_length=50)
    gas_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2) #LITROS


class Municion(models.Model):
    caliber = models.CharField(max_length=50)
    amount = models.IntegerField()


class Armamento(models.Model):
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    ammo = models.ForeignKey(Municion, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField()
    color = models.CharField(max_length=20)


class Candado(models.Model):
    equipment = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20)
    provider = models.CharField(max_length=50)