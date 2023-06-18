from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    dni = models.CharField(max_length=20, unique=True, default=None, null=True)
    birthdate = models.DateField(default=date.today, null=True)
    GENDER_CHOICES = [
        ('masculino','masculino'),
        ('femenino','femenino'),
        ('indefinido','indefinido'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='indefinido', null=True)
    address = models.CharField(max_length=200, default='Ecuador', null=True)
    phone_number = models.CharField(max_length=20)
    isVerified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_operative = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Cliente(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ImagenesPerfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url_img = models.CharField(max_length=100)

class CuentaTelefono(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_cuenta_telefono'

class GroupType(models.Model):
    TYPE_CHOICES = [
        ('administrativo', 'administrativo'),
        ('operativo', 'operativo'),
        ('cliente', 'cliente')
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    

class Cargo(models.Model):
    TYPE_CHOICES = [
        ('administrativo', 'administrativo'),
        ('operativo', 'operativo'),
        ('servicios generales', 'servicios generales')
    ]
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

class Empresa(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ruc = models.CharField(max_length=20)
    policy = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

class Sucursal(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200)

class PersonalAdministrativo(models.Model):
    start_date = models.DateField(default=date.today)
    final_date = models.DateField(default=date.today)
    branch = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    charge = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class PersonalOperativo(models.Model):
    start_date = models.DateField(default=date.today)
    final_date = models.DateField(default=date.today)
    charge = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='administrative_staffs_created')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class TokenVerificacion(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def has_expired(self):
        now = timezone.now()
        return now > self.expiry_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

class PasswordResetVerificacion(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def has_expired(self):
        now = timezone.now()
        return now > self.expiry_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

class CambioCorreo(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    new_email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def has_expired(self):
        now = timezone.now()
        return now > self.expiry_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users_cambio_correo'

class CambioPassword(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    new_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def has_expired(self):
        now = timezone.now()
        return now > self.expiry_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users_cambio_password'