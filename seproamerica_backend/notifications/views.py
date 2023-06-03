from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from .models import TokenFCM
from .serializers import TokenFCMSerializer, OrderClientNotificationSerializer
from firebase_admin import messaging


# Create your views here.
class FCMTokenView(APIView):
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
    
# una vista para crear notificaciones y enviar (accion del admin)
class OrderClientNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_orderclientnotification",]

    def post(self, request):
        serializer = OrderClientNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.validated_data['user'].id
        tokens = list(TokenFCM.objects.filter(user_id=user_id).values_list('token', flat=True))
        title = serializer.validated_data['title']
        message = serializer.validated_data['message']

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            tokens=tokens,
        )
        response = messaging.send_multicast(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
#use FCM to send the notification... <- pribar luego de implementar el envio
# otra vista para obtener las notificaciones (accion del cliente)
