from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.authentication import JWTAuthentication, HasRequiredPermissions
from .models import TokenFCM
from .serializers import TokenFCMSerializer


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