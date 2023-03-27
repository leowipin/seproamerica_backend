from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from .serializers import ServiceSerializer, ServiceStaffSerializer, ServiceEquipmentSerializer, ServiceInfoSerializer
from users.models import Cargo
from services.models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento
from rest_framework.exceptions import NotFound



class ServiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_servicio","change_servicio","delete_servicio","view_servicio",]

    def get_service_by_id(self, service_id):
        try:
            return Servicio.objects.get(id=service_id)
        except Servicio.DoesNotExist:
            raise NotFound({'message': 'Servicio no encontrado.'})

    @transaction.atomic()
    def post(self, request):
        # saving in service model
        service_serializer = ServiceSerializer(data= request.data, partial=True)
        service_serializer.is_valid(raise_exception=True)
        service = service_serializer.save()
        # saving in service_staff model
        staff = request.data['staff']
        is_optional = request.data['is_optional']
        staff_price_per_hour = request.data['staff_price_per_hour']
        staff_base_hours = request.data['staff_base_hours']
        for i in range(len(staff)):
            data = {
                'service': service.id,
                'staff': staff[i],
                'is_optional': is_optional[i],
                'staff_price_per_hour': staff_price_per_hour[i],
                'staff_base_hours': staff_base_hours[i],
            }
            serializer = ServiceStaffSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        # saving in service_equipment model
        equipment = request.data['equipment']
        for e in equipment:
            data = request.data
            data['service'] = service.id
            data['equipment_type'] = e
            serializer = ServiceEquipmentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({'message': 'Servicio creado exitosamente.'}, status=status.HTTP_200_OK)
    
    def get(self, request):
        service_id = request.GET.get('id')
        service = self.get_service_by_id(service_id)
        serializer = ServiceInfoSerializer(service)
        data = serializer.data
        # getting the data of ServicioTipoPersonal model
        service_staff = ServicioTipoPersonal.objects.filter(service_id=service_id)
        staff = []
        is_optional = []
        staff_price_per_hour = []
        staff_base_hours = []
        for ss in service_staff:
            charge = Cargo.objects.get(id=ss.staff_id)
            staff.append(charge.name)
            is_optional.append(ss.is_optional)
            staff_price_per_hour.append(ss.staff_price_per_hour)
            staff_base_hours.append(ss.staff_base_hours)
        data['staff'] = staff
        data['is_optional'] = is_optional
        data['staff_price_per_hour'] = staff_price_per_hour
        data['staff_base_hours'] = staff_base_hours
        # getting the data of ServicioTipoEquipamiento model
        service_equipment = ServicioTipoEquipamiento.objects.filter(service_id = service_id)
        equipment = []
        vehicle_is_optional, lock_is_optional, price_range1, price_range2, price_range3, lower_limit1, upper_limit1, lower_limit2, upper_limit2, lower_limit3, upper_limit3 = [None] * 11
        for se in service_equipment:
            equipment.append(se.equipment_type)
            vehicle_is_optional = se.vehicle_is_optional
            lock_is_optional = se.lock_is_optional
            price_range1 = se.price_range1
            price_range2 = se.price_range2
            price_range3 = se.price_range3
            lower_limit1 = se.lower_limit1
            upper_limit1 = se.upper_limit1
            lower_limit2 = se.lower_limit2
            upper_limit2 = se.upper_limit2
            lower_limit3 = se.lower_limit3
            upper_limit3 = se.upper_limit3
        data['equipment'] = equipment
        data['vehicle_is_optional'] = vehicle_is_optional
        data['lock_is_optional'] = lock_is_optional
        data['price_range1'] = price_range1
        data['price_range2'] = price_range2
        data['price_range3'] = price_range3
        data['lower_limit1'] = lower_limit1
        data['upper_limit1'] = upper_limit1
        data['lower_limit2'] = lower_limit2
        data['upper_limit2'] = upper_limit2
        data['lower_limit3'] = lower_limit3
        data['upper_limit3'] = upper_limit3

        return Response(data, status=status.HTTP_200_OK)
    
    @transaction.atomic()
    def put(self, request):
        service_id = request.data.get('id')
        service = self.get_service_by_id(service_id)
        service_serializer = ServiceSerializer(service, data=request.data, partial=True)
        service_serializer.is_valid(raise_exception=True)
        service_serializer.save()
        # updating ServicioTipoPersonal model
        service_staff = ServicioTipoPersonal.objects.filter(service_id = service_id)
        staff = request.data.get('staff')
        is_optional = request.data['is_optional']
        staff_price_per_hour = request.data['staff_price_per_hour']
        staff_base_hours = request.data['staff_base_hours']
        staff_size = len(staff)
        service_staff_size = len(service_staff)
        for i in range(staff_size):
            data = {
                    'service': service_id,
                    'staff': staff[i],
                    'is_optional': is_optional[i],
                    'staff_price_per_hour': staff_price_per_hour[i],
                    'staff_base_hours': staff_base_hours[i],
                }
            if i <= service_staff_size-1:
                serializer_staff = ServiceStaffSerializer(service_staff[i], data=data)
                serializer_staff.is_valid(raise_exception=True)
                serializer_staff.save()
            elif i > service_staff_size-1:
                serializer_staff = ServiceStaffSerializer(data=data, partial=True)
                serializer_staff.is_valid(raise_exception=True)
                serializer_staff.save()
        if service_staff_size > staff_size:
            for i in range(staff_size, service_staff_size):
                service_staff[i].delete()
        # updating ServicioTipoEquipamiento model
        service_equipment = ServicioTipoEquipamiento.objects.filter(service_id = service_id)
        equipment = request.data.get('equipment')
        equipment_size = len(equipment)
        service_equipment_size = len(service_equipment)
        for i in range(equipment_size):
            data = request.data
            data['service'] = service_id
            data['equipment_type'] = equipment[i]
            if i <= service_equipment_size-1:
                serializer_equipment = ServiceEquipmentSerializer(service_equipment[i], data=data)
                serializer_equipment.is_valid(raise_exception=True)
                serializer_equipment.save()
            elif i > service_equipment_size-1:
                serializer_equipment = ServiceEquipmentSerializer(data=data, partial=True)
                serializer_equipment.is_valid(raise_exception=True)
                serializer_equipment.save()
        if service_equipment_size > equipment_size:
            for i in range(equipment_size, service_equipment_size):
                print(i)
                service_equipment[i].delete()

        return Response({'message': 'Servicio actualizado exitosamente.'}, status=status.HTTP_200_OK)
        
    def delete(self, request):
        service_id = request.GET.get('id')
        service = self.get_service_by_id(service_id)
        service.delete()
        return Response({'message': 'Servicio eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        #probar