from rest_framework import serializers
from .models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento, Pedido, PedidoPersonal, PedidoEquipamiento, PersonalAsignado, EquipamientoAsignado, Facturacion
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

class OrderPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('start_date', 'start_time', 'end_date', 'end_time', 'duration', 'total', 'payment_method', 'status', 'origin_lat', 'origin_lng', 'destination_lat', 'destination_lng', 'phone_account')

class AssignedStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAsignado
        fields = '__all__'

class AssignedEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipamientoAsignado
        fields = '__all__'

class OrderAllSerializer(serializers.ModelSerializer):
    client_first_name = serializers.CharField(source='client.user.first_name')
    client_last_name = serializers.CharField(source='client.user.last_name')
    client_dni = serializers.CharField(source='client.user.dni')
    service_name = serializers.CharField(source='service.name')
    class Meta:
        model = Pedido
        fields = ('id', 'date_request', 'start_date', 'start_time', 'client_first_name', 'client_last_name', 'client_dni', 'service_name')

class OrderRestSerializer(serializers.ModelSerializer):
    client_first_name = serializers.CharField(source='client.user.first_name')
    client_last_name = serializers.CharField(source='client.user.last_name')
    client_dni = serializers.CharField(source='client.user.dni')
    service_name = serializers.CharField(source='service.name')
    class Meta:
        model = Pedido
        fields = ('id', 'date_request', 'start_date', 'start_time', 'client_first_name', 'client_last_name', 'client_dni', 'service_name', 'status')

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facturacion
        fields = '__all__'