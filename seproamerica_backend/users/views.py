from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignUpSerializer, GroupSerializer, AdminStaffSerializer, SignInSerializer, OperationalStaffSerializer, ClientSerializer, UserSerializer, AdminInfoSerializer, OperationalInfoSerializer, ClientSignUpSerializer
from users.models import Usuario,  Cliente, PersonalAdministrativo, PersonalOperativo, PasswordResetVerificacion
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
                subject = 'Welcome to Seproamérica!'
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

        token = generate_token(user)

        return Response({
            "token": token
        }, status=status.HTTP_200_OK)

class ClientView(APIView): # view for the actions that the client can perform for their own data
    pass

class ClientListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cliente']

    def get(self, request):
        clients = Usuario.objects.filter(is_staff=False)
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data)


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


class OperationalSignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = generate_token(user)

        if not user.is_operative:
            return Response({'message':'No tiene cuenta de personal operativo'}, status=status.HTTP_403_FORBIDDEN)

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
                return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(adminSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.GET.get('id')
        try:
            adminstaff = PersonalAdministrativo.objects.select_related('user').get(user_id=user_id)
            serializer = AdminInfoSerializer(adminstaff)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response({'message': f'Usuario con id {user_id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class AdminListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_personaladministrativo']

    def get(self, request):
        admins = PersonalAdministrativo.objects.all()
        users_admins = Usuario.objects.filter(personaladministrativo__in=admins)
        serializer = UserSerializer(users_admins, many=True)
        return Response(serializer.data)

class AdminClientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_cliente','delete_cliente']

    def get(self, request):
        user_id = request.GET.get('id')
        try:
            client = Cliente.objects.select_related('user').get(user_id=user_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response({'message': f'Usuario con id {user_id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        pass


class OperationalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_personaloperativo","change_personaloperativo","delete_personaloperativo","view_personaloperativo",]

    @transaction.atomic()
    def post(self, request):
        userSerializer = SignUpSerializer(data = request.data, context={'group_name': request.data.get('group')})
        if userSerializer.is_valid():
            user = userSerializer.save()
            user.is_staff = True
            user.is_operative = True
            user.save()
            request.data['user'] = user.id
            request.data['created_by'] = request.user
            operationalSerializer = OperationalStaffSerializer(data=request.data)
            if operationalSerializer.is_valid():
                opUser = operationalSerializer.save()
                opUser.save()
                return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response(operationalSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.GET.get('id')
        try:
            opstaff = PersonalOperativo.objects.select_related('user').get(user_id=user_id)
            serializer = OperationalInfoSerializer(opstaff)
            return Response(serializer.data)
        except PersonalOperativo.DoesNotExist:
            return Response({'message': f'Personal operativo con id {user_id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class OperationalListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_personaloperativo']

    def get(self, request):
        ops = PersonalOperativo.objects.all()
        users_op = Usuario.objects.filter(personaloperativo__in=ops)
        serializer = UserSerializer(users_op, many=True)
        return Response(serializer.data)


class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            verification_token = TokenVerificacion.objects.get(token=token)
            if verification_token.has_expired():
                context = {'verification_successful': False, 'message': 'Tu link de verificación ha expirado, por favor vuelve a registrarte.'}
                return render(request, 'verificationResult.html', context)
            user = verification_token.user
            user.isVerified = True
            user.save()
            verification_token.delete()
            context = {'verification_successful': True, 'message': 'Verificación exitosa'}
            return render(request, 'verificationResult.html', context)
        except TokenVerificacion.DoesNotExist:
            context = {'verification_successful': False, 'message': 'Verificación fallida'}
            return render(request, 'verificationResult.html', context)

class GroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['add_group','change_group','delete_group']
    def post(self, request):
        permissions = request.data['permissions']
        for i in range(len(permissions)):
            codename = perms_spanishtoenglish(permissions[i])
            permissions[i] = codename

        group_type = request.data['group_type']
        if group_type == 'admin':
            request.data['name'] = "admin_" + request.data['name']
        elif group_type == 'op':
            request.data['name'] = "op_" + request.data['name']
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.permissions.set(serializer.validated_data['permissions'])
            return Response({'message': 'Group created successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        group_name = request.GET.get('name')

        if not group_name:
            return Response({'message': 'Nombre del grupo no enviado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group)
        permissions = serializer.data['permissions']
        for i in range(len(permissions)):
            codename = perms_englishtospanish(permissions[i])
            permissions[i] = codename

        return Response(serializer.data, status=status.HTTP_200_OK)

class GroupListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.values_list('name', flat=True)
        return Response({"groups": list(groups)})


class AdminGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.filter(name__contains='admin').values_list('name', flat=True)
        return Response({"groups": list(groups)})

class OperationalGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']

    def get(self, request):
        groups = Group.objects.filter(name__contains='op').values_list('name', flat=True)
        return Response({"groups": list(groups)})

class PermissionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ['view_group']
    def get(self, request):
        content_types = ContentType.objects.filter(app_label__in=['users', 'auth']).exclude(model__in=['tokenverificacion', 'permission'])
        permissions = []
        for content_type in content_types:
            content_type_permissions = Permission.objects.filter(content_type=content_type)
            codenames = []
            for p in content_type_permissions:
                codename = perms_englishtospanish(p.codename)
                codenames.append(codename)
            permissions.extend(codenames)

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
                return Response({'message': 'El token ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetVerificacion.DoesNotExist:
            return Response({'message': 'El token no es válido'}, status=status.HTTP_400_BAD_REQUEST)

        user = token_instance.user
        user.set_password(password)
        user.save()

        token_instance.delete()

        return Response({'message': 'Contraseña restablecida exitosamente'}, status=status.HTTP_200_OK)