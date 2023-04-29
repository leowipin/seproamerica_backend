from django.db import models
from users.models import Cliente

class Cardauth(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    token = models.CharField(max_length=20, unique=True)
    card_number = models.CharField(max_length=6)