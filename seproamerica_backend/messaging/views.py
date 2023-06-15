from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from firebase_admin import firestore
from rest_framework import status
from users.authentication import JWTAuthentication

User = get_user_model()

class SendMessageView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.user
        user = User.objects.get(id=user_id)
        group = user.groups.first()
        sender_role = group.name

        data = {
            'sender': user_id,
            'sender_role': sender_role,
            'message': request.data.get('message')
        }

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        if sender_role == 'cliente':
            doc_id = user_id
        else:
            doc_id = request.data.get('client_id')

        db = firestore.client()
        doc_ref = db.collection('mensajeria').document(str(doc_id))
        doc_ref.update({
            'fecha_ultimo_mensaje': message.date_sended,
            'ultimo_mensaje': message.message
        })
        messages_ref = doc_ref.collection('mensajes')
        messages_ref.add({
            'contenido': message.message,
            'fecha_envio': message.date_sended,
            'remitente': sender_role
        })

        return Response({'message': 'Mensaje creado y enviado.'}, status=status.HTTP_201_CREATED)


# Create your views here.
