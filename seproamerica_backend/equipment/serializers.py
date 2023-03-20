from rest_framework import serializers
from users.models import Sucursal
from .models import Equipamiento, Telefono, Municion, Armamento, Candado, Vehiculo

class EquipmentSerializer(serializers.ModelSerializer):
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name', write_only=True)
    class Meta:
        model = Equipamiento
        fields = '__all__'

#PHONE SERIALIZERS

class PhoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Telefono
        fields = '__all__'

class PhoneInfoSerializer(serializers.ModelSerializer):
    branch = serializers.CharField(source='equipment.branch.name')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')

    class Meta:
        model = Telefono
        fields = ('id','branch','brand','model','phone_number','color')

class PhoneListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='equipment_id')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')
    class Meta:
        model = Telefono
        fields = ('id', 'brand', 'model', 'phone_number',)

# WEAPON SERIALIZERS

class WeaponSerializer(serializers.ModelSerializer):
    ammo = serializers.SlugRelatedField(queryset=Municion.objects.all(), slug_field='caliber', write_only=True)

    class Meta:
        model = Armamento
        fields = '__all__'

class WeaponInfoSerializer(serializers.ModelSerializer):
    branch = serializers.CharField(source='equipment.branch.name')
    model = serializers.CharField(source='equipment.model')
    ammo = serializers.CharField(source='ammo.caliber')
    brand = serializers.CharField(source='equipment.brand')

    class Meta:
        model = Armamento
        fields = ('id','branch', 'brand', 'model','serial_number','category','ammo')

class WeaponListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='equipment_id')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')
    caliber = serializers.CharField(source='ammo.caliber')
    class Meta:
        model = Armamento
        fields = ('id','brand', 'model', 'category', 'caliber',)

class AmmoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municion
        fields = '__all__'    

# LOCK SERIALIZERS

class LockSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candado
        fields = '__all__'

class LockInfoSerializer(serializers.ModelSerializer):
    branch = serializers.CharField(source='equipment.branch.name')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')

    class Meta:
        model = Candado
        fields = ('id', 'branch', 'brand', 'model', 'serial_number', 'color')

class LockListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='equipment_id')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')
    class Meta:
        model = Candado
        fields = ('id', 'brand', 'model')

# VEHICLE SERIALIZERS

class VehicleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vehiculo
        fields = '__all__'

class VehicleInfoSerializer(serializers.ModelSerializer):
    branch = serializers.CharField(source='equipment.branch.name')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')

    class Meta:
        model = Vehiculo
        fields = ('id', 'branch', 'brand', 'model', 'category', 'plate', 'year', 'color')

class VehicleListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='equipment_id')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')
    class Meta:
        model = Vehiculo
        fields = ('id', 'brand', 'model', 'category')
