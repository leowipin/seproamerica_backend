from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignUpSerializer, GroupSerializer, AdminStaffSerializer, SignInSerializer, OperationalStaffSerializer, ClientSerializer, UserSerializer, AdminInfoSerializer, OperationalInfoSerializer, ClientSignUpSerializer, ClientPutSerializer, ClientUpdateSerializer, ClientNamesSerializer, PhoneAccountSerializer, PhoneInfoSerializer, PersonalSerializer, ChargeSerializer, BranchSerializer, PhoneNameSerializer, StaffSerializer, AdminPutSerializer, OperationalPutSerializer, CompanySerializer
from users.models import Usuario,  Cliente, PersonalAdministrativo, PersonalOperativo, PasswordResetVerificacion, GroupType, CambioCorreo, CambioPassword, CuentaTelefono, Cargo, Sucursal
from rest_framework import status
from .models import TokenVerificacion
from django.template.loader import render_to_string
from seproamerica_backend import settings
from django.core.mail import EmailMessage
import secrets
from django.shortcuts import render
from users.authentication import JWTAuthentication, HasRequiredPermissions
from django.db import transaction
from users.utils import generate_token, perms_englishtospanish, perms_spanishtoenglish
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password




User = get_user_model()

class SignUpView(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data, context={'group_name': 'cliente'})
        if serializer.is_valid():
            user = serializer.save()
            request.data['user'] = user.id
            clientSerializer = ClientSignUpSerializer(data = request.data)
            if clientSerializer.is_valid():
                clientUser = clientSerializer.save()
                clientUser.save()

                 # generate verification token
                verification_token = secrets.token_hex(16)

                # save verification token to database
                TokenVerificacion.objects.create(user=user, token=verification_token)

                # send verification email
                context = {'name': user.first_name, 'verification_token': verification_token, 'HOST_URL':settings.HOST_URL}
                html_content = render_to_string('signupEmail.html', context)
                subject = 'Bienvenido Seproamérica!'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [user.email]
                email = EmailMessage(subject, html_content, from_email, to)
                email.content_subtype = 'html'

                try:
                    email.send()
                except Exception as e:
                    print(e)
                    return Response({'message': 'Error al enviar el email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                user.save()
                return Response({'message': 'Email de verificación enviado'}, status=status.HTTP_200_OK)
            else:
                return Response(clientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientSignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if not user.isVerified:
            return Response({'message': 'Cuenta no verificada.'}, status=status.HTTP_403_FORBIDDEN)
        
        if not user.is_active:
            return Response({'message':'Su cuenta está inactiva.'}, status=status.HTTP_403_FORBIDDEN)

        token = generate_token(user)

        return Response({
            "token": token
        }, status=status.HTTP_200_OK)

class ClientView(APIView): # view for the actions that the client can perform for their own data. get, delete and put
    authentication_classes = [JWTAuthentication]

    def get_client(self, user_id):
        return Usuario.objects.get(id=user_id)

    def get(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        serializer = ClientUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        serializer = ClientUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Datos modificados correctamente'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        password = request.GET.get('password')
        hashed_password = user.password
        if not check_password(password, hashed_password):
            return Response({'message': 'Contraseña incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({'message': 'Cuenta eliminada exitosamente.'}, status=status.HTTP_200_OK)
    


class ClientNamesView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_client(self, user_id):
        return Usuario.objects.get(id=user_id)

        
    def get(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        serializer = ClientNamesSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PhoneNameView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_phone(self, user_id):
        return Usuario.objects.get(id=user_id)

    def get(self, request):
        phone_id = request.user
        phone = self.get_phone(phone_id)
        serializer = PhoneNameSerializer(phone)
        first_name = serializer.data['first_name']
        response_data = {'first_name': first_name}
        return Response(response_data, status=status.HTTP_200_OK)
    

class ClientListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cliente']

    def get(self, request):
        clients = Usuario.objects.filter(is_staff=False, dni__isnull=False)
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminSignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if not user.is_admin:
            return Response({'message':'No tiene cuenta de administrador'}, status=status.HTTP_403_FORBIDDEN)

        token = generate_token(user)
        return Response({
            "token": token
        }, status=status.HTTP_200_OK)


class PhoneAccountSignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = generate_token(user)

        return Response({
            "token": token
        }, status=status.HTTP_200_OK)


class AdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_personaladministrativo","change_personaladministrativo","delete_personaladministrativo","view_personaladministrativo",]

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

    def get(self, request):
        user_id = request.GET.get('id')
        try:
            adminstaff = PersonalAdministrativo.objects.select_related('user').get(user_id=user_id)
            serializer = AdminInfoSerializer(adminstaff)
            data = serializer.data
            data['id'] = user_id
            return Response(data,  status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({'message': 'Personal administrativo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        user_id = request.data.get('id')
        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({'message': 'Personal administrativo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        group_name = request.data.get('group')
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        user_group = User.groups.through.objects.get(usuario=user)
        user_group.group_id = group.id
        user_group.save()
        hashed_password = make_password(request.data.get('password'))
        request.data['password'] = hashed_password
        user_serializer = AdminPutSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            request.data['user'] = user.id
            try:
                personal_admin = PersonalAdministrativo.objects.get(user_id=user_id)
            except PersonalAdministrativo.DoesNotExist:
                return Response({'message': 'Personal administrativo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            admin_serializer = AdminStaffSerializer(personal_admin, data=request.data)
            if admin_serializer.is_valid():
                adminUser = admin_serializer.save()
                return Response({'message': 'Personal administrativo actualizado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_personaladministrativo']

    def get(self, request):
        admins = PersonalAdministrativo.objects.all()
        users_admins = Usuario.objects.filter(personaladministrativo__in=admins)
        serializer = StaffSerializer(users_admins, many=True)
        return Response(serializer.data)

class AdminClientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cliente','delete_cliente']

    def get_client(self, user_id):
        try:
            client = Cliente.objects.select_related('user').get(user_id=user_id)
            return client
        except Cliente.DoesNotExist:
            raise NotFound({'message': 'Cliente no encontrado.'})
        
    def get(self, request):
        user_id = request.GET.get('id')
        try:
            client = Cliente.objects.select_related('user').get(user_id=user_id)
            serializer = ClientSerializer(client)
            data = serializer.data
            data['id'] = user_id
            return Response(data,  status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({'message': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_id = request.data.get('id')
        client = self.get_client(user_id)
        serializer = ClientPutSerializer(client.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cliente modificado correctamente'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user_id = request.GET.get('id')
        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({'message': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'Cliente eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        
        


class OperationalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_personaloperativo","change_personaloperativo","delete_personaloperativo","view_personaloperativo",]

    @transaction.atomic()
    def post(self, request):
        request.data['password'] = 'empleado'
        userSerializer = SignUpSerializer(data = request.data, context={'group_name': 'empleado'})
        if userSerializer.is_valid():
            user = userSerializer.save()
            user.is_staff = True
            user.is_operative = True
            user.is_active = False
            user.save()
            request.data['user'] = user.id
            request.data['created_by'] = request.user
            operationalSerializer = OperationalStaffSerializer(data=request.data)
            if operationalSerializer.is_valid():
                opUser = operationalSerializer.save()
                opUser.save()
                return Response({'message': 'Empleado creado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(operationalSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.GET.get('id')
        try:
            opstaff = PersonalOperativo.objects.select_related('user').get(user_id=user_id)
            serializer = OperationalInfoSerializer(opstaff)
            data = serializer.data
            data['id'] = user_id
            return Response(data,  status=status.HTTP_200_OK)
        except PersonalOperativo.DoesNotExist:
            return Response({'message': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        user_id = request.data.get('id')
        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({'message': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = OperationalPutSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            request.data['user'] = user.id
            try:
                personal_operative = PersonalOperativo.objects.get(user_id=user_id)
            except PersonalOperativo.DoesNotExist:
                return Response({'message': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            operative_serializer = OperationalStaffSerializer(personal_operative, data=request.data)
            if operative_serializer.is_valid():
                opUser = operative_serializer.save()
                return Response({'message': 'Empleado actualizado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(operative_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OperationalListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_personaloperativo']

    def get(self, request):
        ops = PersonalOperativo.objects.all()
        users_op = Usuario.objects.filter(personaloperativo__in=ops)
        serializer = StaffSerializer(users_op, many=True)
        return Response(serializer.data)
    

class PersonalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_personaloperativo', 'view_personaladministrativo', 'delete_personaladministrativo', 'delete_personaloperativo']

    def get(self, request):
        queryset = Usuario.objects.filter(is_staff=True, dni__isnull=False, is_superuser=False)
        serializer = PersonalSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user_id = request.GET.get('id')
        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({'message': 'Personal no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'Personal eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class PhoneAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_cuentatelefono","change_cuentatelefono","delete_cuentatelefono","view_cuentatelefono",]

    def get_phone_by_id(self, phone_id):
        try:
            return Usuario.objects.get(id=phone_id)
        except Usuario.DoesNotExist:
            raise NotFound({'message': 'Cuenta no encontrada.'})
    
    @transaction.atomic()
    def post(self, request):
        serializer = SignUpSerializer(data=request.data, partial=True, context={'group_name': 'operador'})
        serializer.is_valid(raise_exception=True)
        serializer.is_operative = True
        account = serializer.save()
        account.first_name = request.data.get('first_name')
        account.is_operative = True
        account.birthdate = None
        account.address = None
        account.gender = None
        account.save()
        request.data['user'] = account.id
        serializer2 = PhoneAccountSerializer(data=request.data)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()
        return Response({'message': 'Cuenta creada correctamente.'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        phone_id = request.GET.get('id')
        phone = self.get_phone_by_id(phone_id)
        serializer = PhoneInfoSerializer(phone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        phone_id = request.data.get('id')
        phone = self.get_phone_by_id(phone_id)
        hashed_password = make_password(request.data.get('password'))
        request.data['password'] = hashed_password
        serializer = PhoneInfoSerializer(phone, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cuenta modificada exitosamente'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        phone_id = request.GET.get('id')
        phone = self.get_phone_by_id(phone_id)
        phone.delete()
        return Response({'message': 'Cuenta eliminada correctamente.'},status=status.HTTP_204_NO_CONTENT)
        

class PhoneAccountList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cuentatelefono']
    
    def get(self, request):
        phone = CuentaTelefono.objects.all()
        users_phone = Usuario.objects.filter(cuentatelefono__in=phone)
        serializer = PhoneInfoSerializer(users_phone, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChargeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['add_cargo','change_cargo','delete_cargo','view_cargo']

    def get_charge_by_id(self, charge_id):
        try:
            return Cargo.objects.get(id=charge_id)
        except Cargo.DoesNotExist:
            raise NotFound({'message': 'Cargo no encontrado.'})
    
    def post(self, request):
        serializer = ChargeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cargo creado exitosamente.'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        charge_id = request.GET.get('id')
        charge = self.get_charge_by_id(charge_id)
        serializer = ChargeSerializer(charge)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        charge_id = request.data.get('id')
        charge = self.get_charge_by_id(charge_id)
        serializer = ChargeSerializer(charge, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cargo modificado exitosamente.'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        charge_id = request.GET.get('id')
        charge = self.get_charge_by_id(charge_id)
        charge.delete()
        return Response({'message': 'Cargo eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    

class ChargeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cargo']
    
    def get(self, request):
        charges = Cargo.objects.all()
        serializer = ChargeSerializer(charges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BranchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['add_sucursal','change_sucursal','delete_sucursal','view_sucursal']

    def get_branch_by_id(self, branch_id):
        try:
            return Sucursal.objects.get(id=branch_id)
        except Sucursal.DoesNotExist:
            raise NotFound({'message': 'Sucursal no encontrada.'})

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Sucursal creada exitosamente.'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        branch_id = request.GET.get('id')
        branch = self.get_branch_by_id(branch_id)
        serializer = BranchSerializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        branch_id = request.data.get('id')
        branch = self.get_branch_by_id(branch_id)
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Sucursal modificada exitosamente.'}, status=status.HTTP_200_OK)

    def delete(self, request):
        branch_id = request.GET.get('id')
        branch = self.get_branch_by_id(branch_id)
        branch.delete()
        return Response({'message': 'Sucursal eliminada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    

class BranchListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_sucursal']

    def get(self, request):
        sucursales = Sucursal.objects.all()
        serializer = BranchSerializer(sucursales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            verification_token = TokenVerificacion.objects.get(token=token)
            if verification_token.has_expired():
                context = {'title': 'Verificación de correo', 'message': 'Tu enlace de verificación ha expirado, por favor vuelve a registrarte.'}
                return render(request, 'verificationResult.html', context)
            user = verification_token.user
            user.isVerified = True
            user.save()
            verification_token.delete()
            context = {'title': 'Verificación de correo', 'message': 'Verificación exitosa! Tu solicitud ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)
        except TokenVerificacion.DoesNotExist:
            context = {'title': 'Verificación de correo', 'message': 'Verificación fallida. Lo sentimos, Tu solicitud no ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)

class GroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['add_group','change_group','delete_group']
    def post(self, request):
        permissions = request.data['permissions']
        for i in range(len(permissions)):
            name = perms_spanishtoenglish(permissions[i])
            permissions[i] = name

        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.permissions.set(serializer.validated_data['permissions'])
            GroupType.objects.create(group=group, type=request.data['group_type'])
            return Response({'message': 'Grupo creado exitosamente'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        group_id = request.GET.get('id')

        if not group_id:
            return Response({'message': 'ID del grupo no enviado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group)
        permissions = serializer.data['permissions']
        for i in range(len(permissions)):
            name = perms_englishtospanish(permissions[i])
            permissions[i] = name
            
        group_type = GroupType.objects.filter(group=group).values_list('type', flat=True).first()
        data = serializer.data
        data['group_type'] = group_type

        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request):
        group_id = request.data.get('id')
        if not group_id:
            return Response({'message': 'ID del grupo no enviado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        group_type = request.data.pop('group_type')
        permissions = request.data.get('permissions')
        if permissions:
            for i in range(len(permissions)):
                name = perms_spanishtoenglish(permissions[i])
                permissions[i] = name

        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            group_type_instance = GroupType.objects.get(group=group)
            group_type_instance.type = group_type
            group_type_instance.save()
            group = serializer.save()
            group.permissions.set(serializer.validated_data['permissions'])
            return Response({'message': 'Grupo modificado exitosamente'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        group_id = request.GET.get('id')
        if not group_id:
            return Response({'message': 'ID del grupo no enviado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        group.delete()
        return Response({'message': 'Grupo eliminado correctamente'},status=status.HTTP_204_NO_CONTENT)

class GroupListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.all()
        group_list = []
        for group in groups:
            if not group.name == 'empleado':
                group_type = GroupType.objects.get(group=group).type
                group_list.append({
                    'id': group.id,
                    'name': group.name,
                    'group_type': group_type,
                })
        return Response(group_list)


class AdminGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.filter(grouptype__type='administrativo').values_list('name', flat=True)
        return Response({"groups": list(groups)})

class OperationalGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.filter(grouptype__type='operativo').values_list('name', flat=True)
        return Response({"groups": list(groups)})

class PermissionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']
    def get(self, request):
        content_types = ContentType.objects.filter(app_label__in=['users', 'auth']).exclude(model__in=['tokenverificacion', 'permission','passwordresetverificacion', 'grouptype', 'usuario'])
        permissions = []
        for content_type in content_types:
            content_type_permissions = Permission.objects.filter(content_type=content_type)
            names = []
            for p in content_type_permissions:
                name = perms_englishtospanish(p.name)
                names.append(name)
            permissions.extend(names)

        return Response({'permissions': permissions})


class PasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'message': 'Correo no registrado'}, status=status.HTTP_404_NOT_FOUND)

        token_sent = PasswordResetVerificacion.objects.filter(user__email=email).exists()

        if token_sent:
            return Response({'message': 'Token de verificación ya ha sido enviado'}, status=status.HTTP_400_BAD_REQUEST)


        # generate verification token
        verification_token = secrets.token_hex(3)

        # save verification token to database
        PasswordResetVerificacion.objects.create(user=user, token=verification_token)

        # send verification email
        context = {'name': user.first_name, 'verification_token': verification_token, 'HOST_URL':settings.HOST_URL}
        html_content = render_to_string('passwordResetEmail.html', context)
        subject = 'Restablecimiento de contraseña de Seproamérica'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]
        email = EmailMessage(subject, html_content, from_email, to)
        email.content_subtype = 'html'

        try:
            email.send()
        except Exception as e:
            print(e)
            return Response({'message': 'Error al enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Correo para restablecimiento de contraseña enviado'}, status=status.HTTP_200_OK)

class ChangePassword(APIView):
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            token_instance = PasswordResetVerificacion.objects.get(token=token)
            if token_instance.has_expired():
                return Response({'message': 'El código ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetVerificacion.DoesNotExist:
            return Response({'message': 'El código no es válido'}, status=status.HTTP_400_BAD_REQUEST)

        user = token_instance.user
        user.set_password(password)
        user.save()

        token_instance.delete()

        return Response({'message': 'Contraseña restablecida exitosamente'}, status=status.HTTP_200_OK)
    
class ChangeEmail(APIView):
    authentication_classes = [JWTAuthentication]

    def get_client(self, user_id):
        return Usuario.objects.get(id=user_id)
    
    def post(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        new_email = request.data.get('email')

        token_sent = CambioCorreo.objects.filter(new_email=new_email).exists()

        if token_sent:
            return Response({'message': 'El correo ya ha sido enviado.'}, status=status.HTTP_400_BAD_REQUEST)


        # generate verification token
        verification_token = secrets.token_hex(16)

        # save verification token to database
        CambioCorreo.objects.create(user=user, token=verification_token, new_email = new_email)

        # send verification email
        context = {'name': user.first_name, 'verification_token': verification_token, 'HOST_URL':settings.HOST_URL}
        html_content = render_to_string('changeEmail.html', context)
        subject = 'Cambio de correo Seproamérica'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [new_email]
        email = EmailMessage(subject, html_content, from_email, to)
        email.content_subtype = 'html'

        try:
            email.send()
        except Exception as e:
            print(e)
            return Response({'message': 'Error al enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Correo enviado'}, status=status.HTTP_200_OK)
    
class VerifyNewEmail(APIView):
    def get(self, request, token):
        try:
            verification_token = CambioCorreo.objects.get(token=token)
            if verification_token.has_expired():
                context = {'title': 'Confirmación de correo', 'message': 'Tu enlace de confirmación ha expirado, por favor vuelve a registrarte.'}
                return render(request, 'verificationResult.html', context)
            user = verification_token.user
            user.email = verification_token.new_email
            user.save()
            verification_token.delete()
            context = {'title': 'Confirmación de correo', 'message': '¡Confirmación exitosa! Tu solicitud ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)
        except TokenVerificacion.DoesNotExist:
            context = {'title': 'Confirmación de correo', 'message': 'Confirmación fallida. Lo sentimos, Tu solicitud no ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)
        except IntegrityError as e:
            context = {'title': 'Confirmación de correo', 'message': 'Confirmación fallida. Ya existe un usuario con este correo electrónico.'}
            return render(request, 'verificationResult.html', context)
        except Exception as e:
            context = {'title': 'Confirmación de correo', 'message': 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo más tarde.'}
            return render(request, 'verificationResult.html', context)
        

class ChangeNewPassword(APIView):
    authentication_classes = [JWTAuthentication]

    def get_client(self, user_id):
        return Usuario.objects.get(id=user_id)
    
    def post(self, request):
        user_id = request.user
        user = self.get_client(user_id)
        new_password = request.data.get('new_password')
        password = request.data.get('password')

        if not check_password(password, user.password):
            return Response({'message': 'Su contraseña actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

        token_sent = CambioPassword.objects.filter(user=user_id).exists()

        if token_sent:
            return Response({'message': 'El correo ya ha sido enviado.'}, status=status.HTTP_400_BAD_REQUEST)


        # generate verification token
        verification_token = secrets.token_hex(16)

        # save verification token to database
        CambioPassword.objects.create(user=user, token=verification_token, new_password = make_password(new_password))

        # send verification email
        context = {'name': user.first_name, 'verification_token': verification_token, 'HOST_URL':settings.HOST_URL}
        html_content = render_to_string('changePassword.html', context)
        subject = 'Cambio de contraseña Seproamérica'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]
        email = EmailMessage(subject, html_content, from_email, to)
        email.content_subtype = 'html'

        try:
            email.send()
        except Exception as e:
            print(e)
            return Response({'message': 'Error al enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Correo enviado'}, status=status.HTTP_200_OK)

class VerifyNewPassword(APIView):
    def get(self, request, token):
        try:
            verification_token = CambioPassword.objects.get(token=token)
            if verification_token.has_expired():
                context = {'title': 'Confirmación de contraseña', 'message': 'Tu enlace de confirmación ha expirado, por favor vuelve a registrarte.'}
                return render(request, 'verificationResult.html', context)
            user = verification_token.user
            user.password = verification_token.new_password
            user.save()
            verification_token.delete()
            context = {'title': 'Confirmación de contraseña', 'message': '¡Confirmación exitosa! Tu solicitud ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)
        except TokenVerificacion.DoesNotExist:
            context = {'title': 'Confirmación de contraseña', 'message': 'Confirmación fallida. Lo sentimos, Tu solicitud no ha sido procesada correctamente.'}
            return render(request, 'verificationResult.html', context)
        except Exception as e:
            context = {'title': 'Confirmación de correo', 'message': 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo más tarde.'}
            return render(request, 'verificationResult.html', context)
        
class CompanyView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_empresa",]

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Información guardada correctamente'}, status=status.HTTP_200_OK)
    
# NOTIFICACIONES
    
"""class FCMTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_tokenfcm","add_tokenfcm",]

    def post(self, request):
        user_id = request.user
        data = request.data.copy()
        data['user'] = user_id
        serializer = TokenFCMSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = data.get('token')
        if TokenFCM.objects.filter(token=token, user=user_id).exists():
            return Response({'message': 'El token ya está registrado para este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'Token registrado.'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.GET.get('id')
        tokens = TokenFCM.objects.filter(user_id=user_id)
        serializer = TokenFCMSerializer(tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomNotificationView(APIView): #Notificacion referente a la solicitud de servicio
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_notificacionespersonalizadas","add_notificacionespersonalizadas",]

    def post(self, request): #METODO QUE EL ADMIN USA PARA ENVIAR UNA NOTIFICACION A UN CLIENTE ESPECIFICO CUANDO ACEPTA LA SOLICITUD DE SERVICIO
        serializer = CustomNotificationSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # si se guarda la notificacion en la base proceder a enviar la notificacion
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request): #METODO QUE USA EL CLIENTE PARA OBTENER TODAS SUS NOTIFICACIONES PERSONALIZDAS CUANDO HACE CLIC EN EL BOTON DE NOTIFICACIONES
        user_id = request.user
        notificaciones = NotificacionesPersonalizadas.objects.filter(user_id=user_id)
        serializer = CustomNotificationSerializer(notificaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopicNotificationView(APIView):
    #ESTO PARA LA NOTIFICACION MASIVA DEL ADMINISTRADOR PARA EL CLIENTE (topic:cliente) 2 modelos
    #crear una vista que guarde la notificacion masiva cuyo tema es cliente 1er modelo
    #luego crear otra vista que se obtenga el nombre de todas las notificaciones masivas 2do modelo
    # y en la misma vista que guardo la notificacion masiva puedo hacer el get de la notificacion masiva por id
    # similar a como he estado trabajando con usuarios servicios y recursos
    

    #NOTIFICACION DEDICADA DEL ADMIN A UN CLIENTE ESPECIFICO CUANDO ACEPTA O ELIMINA LA SOLICITUD DE SERVICIO 1 modelo
    #la notificacion dedicada debe tener asociado el pedido
    #NOTIFICACION MASIVA DEL CLIENTE PAL ADMIN CUANDO SOLICITA UN SERVICIO (topic:admin)
    #pensar...
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_notificacionespersonalizadas","add_notificacionespersonalizadas",]"""