from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from .serializers import ServiceSerializer, ServiceStaffSerializer, ServiceEquipmentSerializer, ServiceInfoSerializer, ServiceNamesSerializer, OrderSerializer, OrderStaffSerializer, OrderEquipmentSerializer
from users.models import Cargo, Cliente
from services.models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento, Pedido
from rest_framework.exceptions import NotFound
from django.db.models import F



class ServiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_servicio","change_servicio","delete_servicio"]

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
        staff_is_optional = request.data['staff_is_optional']
        staff_number_is_optional = request.data['staff_number_is_optional']
        staff_price_per_hour = request.data['staff_price_per_hour']
        staff_base_hours = request.data['staff_base_hours']
        for i in range(len(staff)):
            data = {
                'service': service.id,
                'staff': staff[i],
                'staff_is_optional': staff_is_optional[i],
                'staff_number_is_optional':staff_number_is_optional[i],
                'staff_price_per_hour': staff_price_per_hour[i],
                'staff_base_hours': staff_base_hours[i],
            }
            serializer = ServiceStaffSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        # saving in service_equipment model
        equipment = request.data['equipment']
        equipment_is_optional = request.data['equipment_is_optional']
        equipment_number_is_optional = request.data['equipment_number_is_optional']
        equipment_price = request.data['equipment_price']
        for i in range(len(equipment)):
            data = request.data
            data['service'] = service.id
            data['equipment_type'] = equipment[i]
            data['equipment_is_optional'] = equipment_is_optional[i]
            data['equipment_number_is_optional'] = equipment_number_is_optional[i]
            data['equipment_price'] = equipment_price[i]

            serializer = ServiceEquipmentSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({'message': 'Servicio creado exitosamente.'}, status=status.HTTP_200_OK)
    
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
        staff_is_optional = request.data['staff_is_optional']
        staff_number_is_optional = request.data['staff_number_is_optional']
        staff_price_per_hour = request.data['staff_price_per_hour']
        staff_base_hours = request.data['staff_base_hours']
        staff_size = len(staff)
        service_staff_size = len(service_staff)
        for i in range(staff_size):
            data = {
                    'service': service_id,
                    'staff': staff[i],
                    'staff_is_optional': staff_is_optional[i],
                    'staff_number_is_optional': staff_number_is_optional[i],
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
        equipment_is_optional = request.data.get('equipment_is_optional')
        equipment_number_is_optional = request.data.get('equipment_number_is_optional')
        equipment_price = request.data.get('equipment_price')
        equipment_size = len(equipment)
        service_equipment_size = len(service_equipment)
        for i in range(equipment_size):
            data = request.data
            data['service'] = service_id
            data['equipment_type'] = equipment[i]
            data['equipment_is_optional'] = equipment_is_optional[i]
            data['equipment_number_is_optional'] = equipment_number_is_optional[i]
            data['equipment_price'] = equipment_price[i]
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
                service_equipment[i].delete()

        return Response({'message': 'Servicio actualizado exitosamente.'}, status=status.HTTP_200_OK)
        
    def delete(self, request):
        service_id = request.GET.get('id')
        service = self.get_service_by_id(service_id)
        service.delete()
        return Response({'message': 'Servicio eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    
class ServiceNamesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_servicio",]

    def get(self, request):
        services = Servicio.objects.all()
        serializer = ServiceNamesSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServiceGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_servicio",]

    def get_service_by_id(self, service_id):
        try:
            return Servicio.objects.get(id=service_id)
        except Servicio.DoesNotExist:
            raise NotFound({'message': 'Servicio no encontrado.'})

    def get(self, request):
        service_id = request.GET.get('id')
        service = self.get_service_by_id(service_id)
        serializer = ServiceInfoSerializer(service)
        data = serializer.data
        # getting the data of ServicioTipoPersonal model
        service_staff = ServicioTipoPersonal.objects.filter(service_id=service_id)
        staff = []
        staff_is_optional = []
        staff_number_is_optional = []
        staff_price_per_hour = []
        staff_base_hours = []
        for ss in service_staff:
            charge = Cargo.objects.get(id=ss.staff_id)
            staff.append(charge.name)
            staff_is_optional.append(ss.staff_is_optional)
            staff_number_is_optional.append(ss.staff_number_is_optional)
            staff_price_per_hour.append(ss.staff_price_per_hour)
            staff_base_hours.append(ss.staff_base_hours)
        data['staff'] = staff
        data['staff_is_optional'] = staff_is_optional
        data['staff_number_is_optional'] = staff_number_is_optional
        data['staff_price_per_hour'] = staff_price_per_hour
        data['staff_base_hours'] = staff_base_hours
        # getting the data of ServicioTipoEquipamiento model
        service_equipment = ServicioTipoEquipamiento.objects.filter(service_id = service_id)
        equipment = []
        equipment_is_optional = []
        equipment_number_is_optional = []
        equipment_price = []
        price_range1, price_range2, price_range3, lower_limit1, upper_limit1, lower_limit2, upper_limit2, lower_limit3, upper_limit3 = [None] * 9
        for se in service_equipment:
            equipment.append(se.equipment_type)
            equipment_is_optional.append(se.equipment_is_optional)
            equipment_number_is_optional.append(se.equipment_number_is_optional)
            equipment_price.append(se.equipment_price)
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
        data['equipment_is_optional'] = equipment_is_optional
        data['equipment_number_is_optional'] = equipment_number_is_optional
        data['equipment_price'] = equipment_price
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
    

class OrderClientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_pedido","delete_pedido","view_pedido",]

    def post(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        data = request.data.copy()
        data['client'] = client.id
        serializerOrder = OrderSerializer(data=data)
        serializerOrder.is_valid(raise_exception=True)
        order = serializerOrder.save()

        for i in range(len(data['staff'])):
            staff_name  = data['staff'][i]
            staff = Cargo.objects.get(name=staff_name).id
            staff_is_optional = data['staff_is_optional'][i]
            staff_selected = data['staff_selected'][i]
            staff_number_optional = data['staff_number_optional'][i]
            staff_number = data['staff_number'][i]

            pedidoPersonalData = {
                'order': order.id,
                'staff': staff,
                'staff_is_optional': staff_is_optional,
                'staff_selected': staff_selected,
                'staff_number_is_optional': staff_number_optional,
                'staff_number': staff_number
            }
            serializerPedidoPersonal = OrderStaffSerializer(data=pedidoPersonalData)
            serializerPedidoPersonal.is_valid(raise_exception=True)
            serializerPedidoPersonal.save()

        for i in range(len(data['equipment'])):
            equipment_type = data['equipment'][i]
            equipment_is_optional = data['equipment_is_optional'][i]
            equipment_selected = data['equipment_selected'][i]
            equipment_number_optional = data['equipment_number_optional'][i]
            equipment_number = data['equipment_number'][i]

            pedidoEquipamientoData = {
                'order': order.id,
                'equipment_type': equipment_type,
                'equipment_is_optional': equipment_is_optional,
                'equipment_selected': equipment_selected,
                'equipment_number_is_optional': equipment_number_optional,
                'equipment_number': equipment_number
            }
            serializerPedidoEquipamiento = OrderEquipmentSerializer(data=pedidoEquipamientoData)
            serializerPedidoEquipamiento.is_valid(raise_exception=True)
            serializerPedidoEquipamiento.save()

        return Response({'message': 'Pedido recibido'}, status=status.HTTP_200_OK)
    
class OrderClientNamesView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        pedidos = Pedido.objects.filter(client=client.id).values('id', 'date_request', 'status', service_name=F('service__name'))
        return Response(data=list(pedidos), status=200)