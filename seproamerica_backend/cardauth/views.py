from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cardauth, Cliente
from .serializers import CardSerializer, ClientSerializer
from users.authentication import JWTAuthentication, HasRequiredPermissions

class CardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRequiredPermissions]
    required_permissions = ["add_cardauth","view_cardauth","delete_cardauth"]

    def post(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        request.data['client'] = client.id
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = serializer.save(client=client)
        return Response({"message": "Tarjeta creada con éxito"}, status=status.HTTP_201_CREATED)

    
    def get(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        
        cards = Cardauth.objects.filter(client=client)
        serializer = CardSerializer(cards, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user_id = request.user
        client = Cliente.objects.get(user_id=user_id)
        card_token = request.GET.get('cardToken')
        try:
            card = Cardauth.objects.get(token=card_token, client=client)
            card.delete()
            return Response({"message": "Tarjeta eliminada con éxito"}, status=status.HTTP_200_OK)
        except Cardauth.DoesNotExist:
            return Response({"message": "Tarjeta no encontrada"}, status=status.HTTP_404_NOT_FOUND)