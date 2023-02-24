from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignUpSerializer
from rest_framework import status

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response('message: Registro exitoso')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)