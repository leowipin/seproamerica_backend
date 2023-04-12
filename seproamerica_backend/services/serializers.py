from rest_framework import serializers
from .models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento, Pedido, PedidoPersonal, PedidoEquipamiento
from users.models import Cargo

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
        
class ServiceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ServiceStaffSerializer(serializers.ModelSerializer):
    staff = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name')
    class Meta:
        model = ServicioTipoPersonal
        fields = '__all__'

class ServiceEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioTipoEquipamiento
        fields = '__all__'

class ServiceNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id', 'name')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class OrderStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonal
        fields = '__all__'

class OrderEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoEquipamiento
        fields = '__all__'