from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from .serializers import ServiceSerializer, ServiceStaffSerializer, ServiceEquipmentSerializer
from users.models import Cargo


class ServiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_servicio","change_servicio","delete_servicio","view_servicio",]

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
        pass


"""
    @transaction.atomic()
    def post(self, request):
        userSerializer = SignUpSerializer(data = request.data, context={'group_name': request.data.get('group')})
        if userSerializer.is_valid():
            user = userSerializer.save()
            user.is_staff = True
            user.is_admin = True
            user.save()
            request.data['user'] = user.id
            adminSerializer = AdminStaffSerializer(data=request.data)
            if adminSerializer.is_valid():
                adminUser = adminSerializer.save()
                adminUser.save()
                return Response({'message': 'Personal administrativo creado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(adminSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
