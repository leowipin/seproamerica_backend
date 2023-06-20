from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from .models import TokenFCM, OrderClientNotification, OrderAdminNotification
from .serializers import TokenFCMSerializer, OrderClientNotificationSerializer, OrderAdminNotificationSerializer, ClientInfoNotificationSerializer, AdminInfoNotificationSerializer
from firebase_admin import messaging
from firebase_admin import firestore



# Create your views here.
class FCMTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_tokenfcm","add_tokenfcm",]

    def post(self, request):
        user_id = request.user
        data = request.data.copy()
        admin = data.get('administrador')
        token = data.get('token')
        if admin=="administrador":
            response = messaging.subscribe_to_topic([token], 'administrador')
        data['user'] = user_id
        serializer = TokenFCMSerializer(data=data)
        serializer.is_valid(raise_exception=True)
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
        saved_noti = serializer.save()
        
        user_id = serializer.validated_data['user'].id

        #in-app notification
        db = firestore.client()
        user_ref = db.collection('notificaciones').document(str(user_id))
        title = serializer.validated_data['title']
        message = serializer.validated_data['message']

        notification = {
            'title': title,
            'message': message
        }
        user_ref.update({
            'notifications': firestore.ArrayUnion([notification])
        })

        #push notification
        tokens = list(TokenFCM.objects.filter(user_id=user_id).values_list('token', flat=True))

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            data={
            'noti_id': str(saved_noti.id)
            },
            tokens=tokens,
        )
        response = messaging.send_multicast(message)

        return Response({'message': 'Notificación enviada.'}, status=status.HTTP_201_CREATED)
    
class OrderAdminNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_orderadminnotification",]

    def post(self, request):
        serializer = OrderAdminNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        title = serializer.validated_data['title']
        message = serializer.validated_data['message']

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            topic='administrador',
        )
        response = messaging.send(message)
        return Response({'message': 'Notificación enviada.'}, status=status.HTTP_201_CREATED)
    
class ClientNotificationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_orderclientnotification", "delete_orderclientnotification"]

    def get(self, request):
        user_id = request.user
        notifications = OrderClientNotification.objects.filter(user=user_id).order_by('-date_sended')
        serializer = ClientInfoNotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user_id = request.user
        notifications = OrderClientNotification.objects.filter(user=user_id)
        notifications.delete()
        return Response({'message': 'Notificaciones eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    
class ClientNotificationDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["delete_orderclientnotification"]
    
    def delete(self, request):
        noti_id = request.GET.get('id')
        try:
            notification = OrderAdminNotification.objects.get(id=noti_id)
            notification.delete()
            return Response({'message': 'Notificación eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)
        except OrderAdminNotification.DoesNotExist:
            return Response({'error': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)


class AdminNotificationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["view_orderadminnotification", "delete_orderadminnotification"]

    def get(self, request):
        notifications = OrderAdminNotification.objects.all().order_by('-date_sended')
        serializer = AdminInfoNotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        notifications = OrderAdminNotification.objects.all()
        notifications.delete()
        return Response({'message': 'Notificaciones eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    
class AdminNotificationDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["delete_orderadminnotification"]

    def delete(self, request):
        noti_id = request.GET.get('id')
        try:
            notification = OrderAdminNotification.objects.get(id=noti_id)
            notification.delete()
            return Response({'message': 'Notificación eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)
        except OrderAdminNotification.DoesNotExist:
            return Response({'error': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)