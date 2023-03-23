from rest_framework import serializers
from .models import Servicio, ServicioTipoPersonal


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ServiceStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioTipoPersonal