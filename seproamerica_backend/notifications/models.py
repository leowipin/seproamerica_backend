from django.db import models
from django.conf import settings
from users.models import Cliente
from services.models import Pedido
from datetime import date

# Create your models here.

class TokenFCM(models.Model):
    token = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MassiveNotifications(models.Model): # para el topic 'cliente'
    name = models.CharField(max_length=124, unique=True)
    url_img = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    last_time_sended = models.DateTimeField(null=True, blank=True)

class OrderClientNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    url_img = models.URLField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_sended = models.DateField(default=date.today)

class OrderAdminNotification(models.Model): # para el topic 'administrador'
    title = models.CharField(max_length=255)
    message = models.TextField()
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    date_sended = models.DateField(default=date.today)

