from rest_framework import serializers
from .models import Cardauth

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardauth
        fields = '__all__'