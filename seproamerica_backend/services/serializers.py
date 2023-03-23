from rest_framework import serializers
from .models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento
from users.models import Cargo

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ServiceStaffSerializer(serializers.ModelSerializer):
    staff = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name', write_only=True)
    class Meta:
        model = ServicioTipoPersonal
        fields = '__all__'

class ServiceEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioTipoEquipamiento
        fields = '__all__'