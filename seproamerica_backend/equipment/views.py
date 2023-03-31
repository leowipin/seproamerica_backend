from django.shortcuts import render
from users.authentication import JWTAuthentication, HasRequiredPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from equipment.serializers import EquipmentSerializer, PhoneInfoSerializer, PhoneSerializer, PhoneListSerializer, AmmoSerializer, WeaponSerializer, WeaponInfoSerializer, WeaponListSerializer, LockSerializer, LockInfoSerializer, LockListSerializer, VehicleSerializer, VehicleInfoSerializer, VehicleListSerializer
from equipment.models import Equipamiento, Municion, Telefono, Armamento, Candado, Vehiculo
from rest_framework.exceptions import NotFound


class EquipmentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["delete_equipamiento",]

    def delete(self, request):
        equipment_id = request.GET.get('id')
        try:
            equipment = Equipamiento.objects.get(id=equipment_id)
        except Equipamiento.DoesNotExist:
            return Response({'message': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        equipment.delete()
        return Response({'message': 'Equipo eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    

class VehicleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_vehiculo","change_vehiculo","delete_vehiculo","view_vehiculo",]

    def get_vehicle_by_id(self, vehicle_id):
        try:
            return Equipamiento.objects.get(id=vehicle_id)
        except Equipamiento.DoesNotExist:
            raise NotFound({'message': 'Vehículo no encontrado.'})
    
    @transaction.atomic()
    def post(self, request):
        request.data['type']='vehículo'
        equipment_serializer = EquipmentSerializer(data=request.data)
        equipment_serializer.is_valid(raise_exception=True)
        equipment = equipment_serializer.save()
        request.data['equipment']=equipment.id
        vehicle_serializer = VehicleSerializer(data=request.data)
        vehicle_serializer.is_valid(raise_exception=True)
        vehicle = vehicle_serializer.save()
        return Response({'message': 'Vehículo creado con éxito'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        equipment_id = request.GET.get('id')
        try:
            vehicle = Vehiculo.objects.select_related('equipment').get(equipment_id=equipment_id)
            serializer = VehicleInfoSerializer(vehicle)
            data = serializer.data
            data['id'] = equipment_id
            return Response(data,  status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'message': 'Vehículo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
    @transaction.atomic()
    def put(self, request):
        equipment_id = request.data.get('id')
        equipment = self.get_vehicle_by_id(equipment_id)
        equipment_serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        equipment_serializer.is_valid(raise_exception=True)
        equipment_save = equipment_serializer.save()
        request.data['equipment'] = equipment_save.id
        try:
            vehicle = Vehiculo.objects.get(equipment=equipment_save)
        except Vehiculo.DoesNotExist:
            return Response({'message': 'Vehículo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        vehicle_serializer = VehicleSerializer(vehicle, data=request.data)
        vehicle_serializer.is_valid(raise_exception=True)
        vehicle = vehicle_serializer.save()

        return Response({'message': 'Vehículo actualizado con éxito.'}, status=status.HTTP_200_OK)
    

class VehicleListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_vehiculo",]
    def get(self, request):
        vehicles = Vehiculo.objects.filter(equipment__type='vehículo')
        serializer = VehicleListSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class LockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_candado","change_candado","delete_candado","view_candado",]

    def get_lock_by_id(self, lock_id):
        try:
            return Equipamiento.objects.get(id=lock_id)
        except Equipamiento.DoesNotExist:
            raise NotFound({'message': 'Candado satelital no encontrado.'})
        
    @transaction.atomic()
    def post(self, request):
        request.data['type']='candado satelital'
        equipment_serializer = EquipmentSerializer(data=request.data)
        equipment_serializer.is_valid(raise_exception=True)
        equipment = equipment_serializer.save()
        request.data['equipment']=equipment.id
        lock_serializer = LockSerializer(data=request.data)
        lock_serializer.is_valid(raise_exception=True)
        lock = lock_serializer.save()

        return Response({'message': 'Candado satelital creado con éxito'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        equipment_id = request.GET.get('id')
        try:
            lock = Candado.objects.select_related('equipment').get(equipment_id=equipment_id)
            serializer = LockInfoSerializer(lock)
            data = serializer.data
            data['id'] = equipment_id
            return Response(data,  status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'message': 'Candado satelital no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    @transaction.atomic()
    def put(self, request):
        equipment_id = request.data.get('id')
        equipment = self.get_lock_by_id(equipment_id)
        equipment_serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        equipment_serializer.is_valid(raise_exception=True)
        equipment_save = equipment_serializer.save()
        request.data['equipment'] = equipment_save.id
        try:
            lock = Candado.objects.get(equipment=equipment_save)
        except Candado.DoesNotExist:
            return Response({'message': 'Candado satelital no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        lock_serializer = LockSerializer(lock, data=request.data)
        lock_serializer.is_valid(raise_exception=True)
        lock = lock_serializer.save()

        return Response({'message': 'Candado satelital actualizado con éxito'}, status=status.HTTP_200_OK)

class LockListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_candado",]
    def get(self, request):
        locks = Candado.objects.filter(equipment__type='candado satelital')
        serializer = LockListSerializer(locks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class WeaponView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_armamento","change_armamento","delete_armamento","view_armamento",]

    def get_weapon_by_id(self, weapon_id):
        try:
            return Equipamiento.objects.get(id=weapon_id)
        except Equipamiento.DoesNotExist:
            raise NotFound({'message': 'Armamento no encontrado.'})
        
    @transaction.atomic()
    def post(self, request):
        request.data['type']='armamento'
        equipment_serializer = EquipmentSerializer(data=request.data)
        equipment_serializer.is_valid(raise_exception=True)
        equipment = equipment_serializer.save()
        request.data['equipment']=equipment.id
        weapon_serializer = WeaponSerializer(data=request.data)
        weapon_serializer.is_valid(raise_exception=True)
        weapon = weapon_serializer.save()

        return Response({'message': 'Armamento creado con éxito'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        equipment_id = request.GET.get('id')
        try:
            weapon = Armamento.objects.select_related('equipment').get(equipment_id=equipment_id)
            serializer = WeaponInfoSerializer(weapon)
            data = serializer.data
            data['id'] = equipment_id
            return Response(data,  status=status.HTTP_200_OK)
        except Armamento.DoesNotExist:
            return Response({'message': 'Armamento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
    @transaction.atomic()
    def put(self, request):
        equipment_id = request.data.get('id')
        equipment = self.get_weapon_by_id(equipment_id)
        equipment_serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        equipment_serializer.is_valid(raise_exception=True)
        equipment_save = equipment_serializer.save()
        request.data['equipment'] = equipment_save.id
        try:
            weapon = Armamento.objects.get(equipment=equipment_save)
        except Armamento.DoesNotExist:
            return Response({'message': 'Armamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        weapon_serializer = WeaponSerializer(weapon, data=request.data)
        weapon_serializer.is_valid(raise_exception=True)
        weapon = weapon_serializer.save()

        return Response({'message': 'Armamento actualizado con éxito'}, status=status.HTTP_200_OK)
    

class WeaponListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_armamento",]
    def get(self, request):
        weapons = Armamento.objects.filter(equipment__type='armamento')
        serializer = WeaponListSerializer(weapons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    

class AmmoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_municion","change_municion","delete_municion","view_municion",]

    def get_ammo_by_id(self, ammo_id):
        try:
            return Municion.objects.get(id=ammo_id)
        except Municion.DoesNotExist:
            raise NotFound({'message': 'Munición no encontrado.'})
    
    def post(self, request):
        serializer = AmmoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Munición creada exitosamente.'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        ammo_id = request.GET.get('id')
        ammo = self.get_ammo_by_id(ammo_id)
        serializer = AmmoSerializer(ammo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        ammo_id = request.data.get('id')
        ammo = self.get_ammo_by_id(ammo_id)
        serializer = AmmoSerializer(ammo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Munición actualizada exitosamente.'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        ammo = request.GET.get('id')
        ammo = self.get_ammo_by_id(ammo)
        ammo.delete()
        return Response({'message': 'Munición eliminada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    

class AmmoListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_municion",]
    def get(self, request):
        ammos = Municion.objects.all()
        serializer = AmmoSerializer(ammos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhoneView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_telefono","change_telefono","delete_telefono","view_telefono",]

    def get_phone_by_id(self, phone_id):
        try:
            return Equipamiento.objects.get(id=phone_id)
        except Equipamiento.DoesNotExist:
            raise NotFound({'message': 'Teléfono no encontrado.'})

    @transaction.atomic()
    def post(self, request):
        request.data['type']='móbil'
        equipment_serializer = EquipmentSerializer(data=request.data)
        equipment_serializer.is_valid(raise_exception=True)
        equipment = equipment_serializer.save()
        request.data['equipment']=equipment.id

        phone_serializer = PhoneSerializer(data=request.data)
        phone_serializer.is_valid(raise_exception=True)
        phone = phone_serializer.save()

        return Response({'message': 'Teléfono creado con éxito'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        equipment_id = request.GET.get('id')
        try:
            phone = Telefono.objects.select_related('equipment').get(equipment_id=equipment_id)
            serializer = PhoneInfoSerializer(phone)
            data = serializer.data
            data['id'] = equipment_id
            return Response(data,  status=status.HTTP_200_OK)
        except Telefono.DoesNotExist:
            return Response({'message': 'Telefono no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
    @transaction.atomic()
    def put(self, request):
        equipment_id = request.data.get('id')
        equipment = self.get_phone_by_id(equipment_id)
        equipment_serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        equipment_serializer.is_valid(raise_exception=True)
        equipment_save = equipment_serializer.save()
        request.data['equipment'] = equipment_save.id
        try:
            phone = Telefono.objects.get(equipment=equipment_save)
        except Telefono.DoesNotExist:
            return Response({'message': 'Teléfono no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        phone_serializer = PhoneSerializer(phone, data=request.data)
        phone_serializer.is_valid(raise_exception=True)
        phone = phone_serializer.save()

        return Response({'message': 'Teléfono actualizado con éxito'}, status=status.HTTP_200_OK)
    
class PhoneListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_telefono",]
    def get(self, request):
        phones = Telefono.objects.filter(equipment__type='móbil')
        serializer = PhoneListSerializer(phones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CategoryView(APIView):
    def get(self, request):
        data = {
            "categories": ["Automóvil", "Motocicleta", "Camioneta", "Furgoneta",  "Todo terreno"]
        }
        return Response(data, status=status.HTTP_200_OK)

class ColorView(APIView):
    def get(self, request):
        data = {
            "colors": ["plateado", "blanco", "negro", "azul", "rojo", "verde"]
        }
        return Response(data, status=status.HTTP_200_OK)

class BrandVehicleView(APIView):
    def get(self, request):
        data = {
            "brands": ["Chevrolet", "Toyota", "Nissan", "Kia", "Hyundai", "Mazda", "Renault", "Ford", "Chery"]
        }
        return Response(data, status=status.HTTP_200_OK)

class EngineView(APIView):
    def get(self, request):
        data = {
            "engines": ["Gasolina", "Diésel", "Híbrido", "Eléctrico"]
        }
        return Response(data, status=status.HTTP_200_OK)