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

class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('service', 'date_request', 'start_date', 'start_time', 'end_date', 'end_time', 'duration', 'total', 'payment_method', 'status', 'origin_lat', 'origin_lng', 'destination_lat', 'destination_lng')

class OrderNamesSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name')
    requires_origin_and_destination = serializers.BooleanField(source='service.requires_origin_and_destination')

    class Meta:
        model = Pedido
        fields = ('id', 'date_request', 'status', 'service_name', 'requires_origin_and_destination')

class OrderStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonal
        fields = '__all__'

class OrderEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoEquipamiento
        fields = '__all__'