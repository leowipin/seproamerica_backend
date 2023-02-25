from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    dni = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField(default=date.today)
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indefinido'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    isVerified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Charge(models.Model):
    TYPE_CHOICES = [
        ('A', 'Administrative'),
        ('O', 'Operative')
    ]
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

class AdministrativeStaff(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('V', 'Vacaciones')
    ]

    start_date = models.DateField(default=date.today)
    final_date = models.DateField(default=date.today)
    branch = models.CharField(max_length=50)
    charge = models.ForeignKey(Charge, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class OperationalStaff(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('V', 'Vacaciones')
    ]

    start_date = models.DateField()
    final_date = models.DateField()
    charge = models.ForeignKey(Charge, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A')
    branch = models.CharField(max_length=50)
    created_by = models.ForeignKey(AdministrativeStaff, on_delete=models.SET_NULL, null=True, blank=True, related_name='administrative_staffs_created')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class VerificationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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



