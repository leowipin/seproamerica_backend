from rest_framework import serializers
from .models import Cardauth
from users.models import Cliente

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardauth
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['current_card']