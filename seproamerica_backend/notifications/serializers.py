from rest_framework import serializers
from .models import TokenFCM

class TokenFCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenFCM
        fields = '__all__'