from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from .serializers import ServiceSerializer, ServiceStaffSerializer, ServiceEquipmentSerializer, ServiceInfoSerializer, ServiceNamesSerializer, OrderSerializer, OrderStaffSerializer, OrderEquipmentSerializer, OrderNamesSerializer, OrderPutSerializer, AssignedStaffSerializer, AssignedEquipmentSerializer, OrderAllSerializer, OrderRestSerializer, BillingSerializer, OrderStatusSerializer, PhoneAccountPedidoSerializer, OrderReportSerializer
from users.models import Cargo, Cliente, PersonalOperativo, CuentaTelefono, Empresa
from services.models import Servicio, ServicioTipoPersonal, ServicioTipoEquipamiento, Pedido, PedidoPersonal, PedidoEquipamiento, PersonalAsignado, EquipamientoAsignado, Facturacion
from equipment.models import Equipamiento
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

    def get_order_by_id(self, order_id):
        try:
            return Pedido.objects.get(id=order_id)
        except Pedido.DoesNotExist:
            raise NotFound({'message': 'Pedido no encontrado.'})
        
    @transaction.atomic()    
    def post(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        data = request.data.copy()
        data['client'] = client.id
        data['phone_account'] = None
        serializerOrder = OrderSerializer(data=data)
        serializerOrder.is_valid(raise_exception=True)
        order = serializerOrder.save()

        for i in range(len(data['staff'])):
            staff_name  = data['staff'][i]
            staff = Cargo.objects.get(name=staff_name).id
            staff_is_optional = data['staff_is_optional'][i]
            staff_selected = data['staff_selected'][i]
            staff_number_is_optional = data['staff_number_is_optional'][i]
            staff_number = data['staff_number'][i]

            pedidoPersonalData = {
                'order': order.id,
                'staff': staff,
                'staff_is_optional': staff_is_optional,
                'staff_selected': staff_selected,
                'staff_number_is_optional': staff_number_is_optional,
                'staff_number': staff_number
            }
            serializerPedidoPersonal = OrderStaffSerializer(data=pedidoPersonalData)
            serializerPedidoPersonal.is_valid(raise_exception=True)
            serializerPedidoPersonal.save()

        for i in range(len(data['equipment'])):
            equipment_type = data['equipment'][i]
            equipment_is_optional = data['equipment_is_optional'][i]
            equipment_selected = data['equipment_selected'][i]
            equipment_number_is_optional = data['equipment_number_is_optional'][i]
            equipment_number = data['equipment_number'][i]

            pedidoEquipamientoData = {
                'order': order.id,
                'equipment_type': equipment_type,
                'equipment_is_optional': equipment_is_optional,
                'equipment_selected': equipment_selected,
                'equipment_number_is_optional': equipment_number_is_optional,
                'equipment_number': equipment_number
            }
            serializerPedidoEquipamiento = OrderEquipmentSerializer(data=pedidoEquipamientoData)
            serializerPedidoEquipamiento.is_valid(raise_exception=True)
            serializerPedidoEquipamiento.save()

        return Response({'message': 'Pedido recibido', 'order_id':order.id}, status=status.HTTP_200_OK)
    
    def get(self, request):
        order_id = request.GET.get('id')
        order = self.get_order_by_id(order_id)
        serializer = OrderSerializer(order)
        data = serializer.data
        try:
            client = Cliente.objects.get(id=data['client'])
            user_client_id = client.user_id
        except Cliente.DoesNotExist:
            return Response({'message': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        data['client'] = user_client_id
        if data['phone_account'] != None:
            try:
                phone_acc = CuentaTelefono.objects.get(id=data['phone_account'])
                user_phone_id = phone_acc.user_id
            except CuentaTelefono.DoesNotExist:
                return Response({'message': 'Cuenta teléfono no encontrada'}, status=status.HTTP_404_NOT_FOUND)
            data['phone_account'] = user_phone_id
        # getting the data of PedidoPersonal
        order_staff = PedidoPersonal.objects.filter(order_id=order_id)
        staff = []
        staff_is_optional = []
        staff_number_is_optional = []
        staff_selected = []
        staff_number = []
        for os in order_staff:
            charge = Cargo.objects.get(id=os.staff_id)
            staff.append(charge.name)
            staff_is_optional.append(os.staff_is_optional)
            staff_number_is_optional.append(os.staff_number_is_optional)
            staff_selected.append(os.staff_selected)
            staff_number.append(os.staff_number)
        data['staff'] = staff
        data['staff_is_optional'] = staff_is_optional
        data['staff_number_is_optional'] = staff_number_is_optional
        data['staff_selected'] = staff_selected
        data['staff_number'] = staff_number
        # getting the data of PedidoEquipamiento
        order_equipment = PedidoEquipamiento.objects.filter(order_id = order_id)
        equipment = []
        equipment_is_optional = []
        equipment_number_is_optional = []
        equipment_selected = []
        equipment_number = []
        for oe in order_equipment:
            equipment.append(oe.equipment_type)
            equipment_is_optional.append(oe.equipment_is_optional)
            equipment_number_is_optional.append(oe.equipment_number_is_optional)
            equipment_selected.append(oe.equipment_selected)
            equipment_number.append(oe.equipment_number)
        data['equipment'] = equipment
        data['equipment_is_optional'] = equipment_is_optional
        data['equipment_number_is_optional'] = equipment_number_is_optional
        data['equipment_selected'] = equipment_selected
        data['equipment_number'] = equipment_number
        #getting the data of EquipamientoAsignado
        order_equipment_assigned = EquipamientoAsignado.objects.filter(order_id = order_id)
        assigned_equipment = []
        if order_equipment_assigned.exists():
            for oea in order_equipment_assigned:
                assigned_equipment.append(oea.equipment.id)
        data['assigned_equipment'] = assigned_equipment
        #getting the data of PersonalAsignado
        order_staff_assigned = PersonalAsignado.objects.filter(order_id = order_id)
        assigned_staff = []
        staff_leader = None
        if order_staff_assigned.exists():
            for osa in order_staff_assigned:
                assigned_staff.append(osa.operational_staff.user.id)
                if osa.is_leader:
                    staff_leader = osa.operational_staff.user.id
        data['assigned_staff'] = assigned_staff
        data['staff_leader'] = staff_leader
        return Response(data, status=status.HTTP_200_OK)
    
    @transaction.atomic()
    def put(self ,request):
        order_id = request.GET.get('id')
        order = self.get_order_by_id(order_id)
        data = request.data.copy()
        try:
            phone_acc = CuentaTelefono.objects.get(user_id=data['phone_account'])
        except CuentaTelefono.DoesNotExist:
            return Response({'message': 'Cuenta teléfono no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        data['phone_account'] = phone_acc.id
        serializer = OrderPutSerializer(order, data= data)
        serializer.is_valid(raise_exception=True)
        order_save = serializer.save()
        data['order'] = order_id

        # updating PedidoPersonal instance
        order_staff = PedidoPersonal.objects.filter(order=order_save).order_by('id')
        if not order_staff:
            return Response({'message': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        for i, order_s in enumerate(order_staff):
            staff_selected = data['staff_selected'][i]
            staff_number = data['staff_number'][i]

            order_staff_data = {
                'order': order_id,
                'staff_selected': staff_selected,
                'staff_number': staff_number
            }
            serializer_order_staff = OrderStaffSerializer(order_s, data=order_staff_data, partial=True)
            serializer_order_staff.is_valid(raise_exception=True)
            serializer_order_staff.save()

        # updating PedidoEquipamiento instance
        order_equipments = PedidoEquipamiento.objects.filter(order=order_save).order_by('id')
        if not order_equipments:
            return Response({'message': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        for i, order_equipment in enumerate(order_equipments):
            equipment_selected = data['equipment_selected'][i]
            equipment_number = data['equipment_number'][i]

            order_equipment_data = {
                'order': order_id,
                'equipment_selected': equipment_selected,
                'equipment_number': equipment_number
            }
            serializer_order_equipment = OrderEquipmentSerializer(order_equipment, data=order_equipment_data, partial=True)
            serializer_order_equipment.is_valid(raise_exception=True)
            serializer_order_equipment.save()
            
        # creating the assigned staff
        PersonalAsignado.objects.filter(order=order_save).delete()
        for staff_id in data['assigned_staff']:
            try:
                op_staff = PersonalOperativo.objects.get(user_id=staff_id)
            except PersonalOperativo.DoesNotExist:
                return Response({'message': 'Al menos un personal operativo no se ha encontrado'}, status=status.HTTP_404_NOT_FOUND)

            is_leader = staff_id == data['staff_leader']
            assigned_staff_data = {
            'operational_staff': op_staff.id,
            'order': order_id,
            'is_leader': is_leader
            }
            serializer_assigned_staff = AssignedStaffSerializer(data=assigned_staff_data)
            serializer_assigned_staff.is_valid(raise_exception=True)
            serializer_assigned_staff.save()

        # creating the assigned equipment
        EquipamientoAsignado.objects.filter(order=order_save).delete()
        for equipment_id in data['assigned_equipment']:
            try:
                equipment = Equipamiento.objects.get(id=equipment_id)
            except Equipamiento.DoesNotExist:
                return Response({'message': 'Al menos un equipamiento no se ha encontrado'}, status=status.HTTP_404_NOT_FOUND)

            assigned_equipment_data = {
            'equipment': equipment.id,
            'order': order_id
            }
            serializer_assigned_equipment = AssignedEquipmentSerializer(data=assigned_equipment_data)
            serializer_assigned_equipment.is_valid(raise_exception=True)
            serializer_assigned_equipment.save()

        return Response({'message': 'Pedido actualizado con éxito'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        order_id = request.GET.get('id')
        order = self.get_order_by_id(order_id)
        data = {
            'status':'eliminado'
        }
        serializer = OrderSerializer(order, data= data, partial=True)
        serializer.is_valid(raise_exception=True)
        order_save = serializer.save()
        return Response({'message': 'Pedido eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class OrderClientNamesView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        pedidos = Pedido.objects.filter(client=client.id).exclude(status__in=['eliminado']).order_by('-date_request')
        serializer = OrderNamesSerializer(pedidos, many=True)
        return Response(data=serializer.data, status=200)
    
class OrderAllView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.all().order_by('-date_request')
        serializer = OrderAllSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderListRestView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.all().exclude(status__in=['pendiente', 'en proceso']).order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderPendingView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='pendiente').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderAcceptedView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='aceptado').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderPaidView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='pagado').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderProcessView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='en proceso').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDeletedView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='eliminado').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderEndedView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='finalizado').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderRefundView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_pedido",]

    def get(self, request):
        orders = Pedido.objects.filter(status='reembolsado').order_by('-date_request')
        serializer = OrderRestSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StatusChangeView (APIView):
    authentication_classes = [JWTAuthentication]
    def put(self, request):
        order_id=request.GET.get('id')
        print(order_id)
        try:
            pedido = Pedido.objects.get(id=order_id)
            pedido.status = request.data['status']
            serializer = OrderStatusSerializer(pedido, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Pedido actualizado con éxito'}, status=status.HTTP_200_OK)
        except Pedido.DoesNotExist:
            return Response({'message': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class BillingCreateView (APIView): #view used by the client
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_facturacion", "view_facturacion"]

    def post(self, request):
        data = request.data
        empresa = Empresa.objects.first()
        if empresa:
            data['empresa'] = empresa.id
        else:
            raise NotFound({'message': 'Empresa no encontrada.'})
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        data['cliente'] = client.id
        serializer = BillingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Datos de facturacion guardados correctamente'}, status=status.HTTP_200_OK)
    
    def get(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        bill = Facturacion.objects.get(cliente=client.id, pedido=request.GET.get('order'))
        serializer = BillingSerializer(bill)
        return Response(serializer.data, status=status.HTTP_200_OK)

# DELETE METHOD
class BillingDelView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["delete_facturacion",]

    def delete(self, request):
        pass

class PhoneAccountOrderView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["change_pedido", "view_pedido",]

    def get(self, request):
        user_id = request.user
        try:
            phone_account = CuentaTelefono.objects.get(user_id=user_id)
            order = Pedido.objects.get(phone_account=phone_account)
            if order.status == 'en proceso':
                assigned_staff = PersonalAsignado.objects.get(order=order, is_leader=True)
                operational_staff_id = assigned_staff.operational_staff_id
                operational_staff = PersonalOperativo.objects.get(id=operational_staff_id)
                user = operational_staff.user
                first_name = user.first_name
                last_name = user.last_name
                serializer = PhoneAccountPedidoSerializer(order)
                data = serializer.data
                data['employee_first_name'] = first_name
                data['employee_last_name'] = last_name
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except CuentaTelefono.DoesNotExist:
            return Response({'message': 'Cuenta teléfono inexistente'}, status=status.HTTP_404_NOT_FOUND)
        except Pedido.DoesNotExist:
            return Response({'message': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class OrderReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_reportepedido",]
    
    def post(self, request):
        serializer = OrderReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Pedido.objects.get(id=serializer.validated_data['order'].id)
        order.status = 'finalizado'
        order.save()
        serializer.save()
        return Response({'message': 'Reporte finalizado exitosamente.'}, status=status.HTTP_201_CREATED)