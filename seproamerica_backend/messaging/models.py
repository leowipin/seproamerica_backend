from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Message(models.Model):
    SENDER_ROLES = (
        ('operador', 'operador'),
        ('administrador', 'administrador'),
        ('cliente', 'cliente'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_role = models.CharField(max_length=50, choices=SENDER_ROLES)
    message = models.TextField()
    date_sended = models.DateTimeField(default=datetime.now)
