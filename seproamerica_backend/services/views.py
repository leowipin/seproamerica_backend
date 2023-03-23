from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from .serializers import ServiceSerializer, ServiceStaffSerializer
from users.models import Cargo


class ServiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_servicio","change_servicio","delete_servicio","view_servicio",]

    @transaction.atomic()
    def post(self, request):
        service_serializer = ServiceSerializer(data= request.data, partial=True)
        service_serializer.is_valid(raise_exception=True)
        service = service_serializer.save()
        #charges = request.data['required_staff']
        #equipments = request.data['required_equipment']
        for charge_name in request.data['required_staff']:
            charge = Cargo.objects.get(name=charge_name)
            data = {
                'service': service.id,
                'charge': charge.id,
            }
            staff_serializer = ServiceStaffSerializer(data=data)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return Response({'message': 'Servicio y personal creados exitosamente.'}, status=status.HTTP_200_OK)


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
