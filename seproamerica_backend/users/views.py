from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignUpSerializer, GroupSerializer, AdminStaffSerializer
from rest_framework import status
from .models import VerificationToken
from django.template.loader import render_to_string
from seproamerica_backend import settings
from django.core.mail import EmailMessage
import secrets

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data, context={'group_name': 'client'})
        if serializer.is_valid():
            user = serializer.save()
            # generate verification token
            verification_token = secrets.token_hex(16)

            # save verification token to database
            VerificationToken.objects.create(user=user, token=verification_token)

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
            return Response('message: Email de verificación enviado', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminCreateView(APIView):
    def post(self, request):
        userSerializer = SignUpSerializer(data = request.data, context={'group_name': 'superadmin'})
        if userSerializer.is_valid():
            user = userSerializer.save()
            user.is_staff = True
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


class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            verification_token = VerificationToken.objects.get(token=token)
            user = verification_token.user
            user.isVerified = True
            user.save()
            verification_token.delete()
            return Response({'message': 'Verificación exitosa'}, status=status.HTTP_200_OK)
        except VerificationToken.DoesNotExist:
            return Response({'message': 'Verificación fallida'}, status=status.HTTP_400_BAD_REQUEST)
        
class GroupView(APIView):
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.permissions.set(serializer.validated_data['permissions'])
            return Response({'message': 'Group created successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)