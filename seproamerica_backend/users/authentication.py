import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from seproamerica_backend import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token')  # assuming token is sent in request body

        if not token:
            raise AuthenticationFailed('Token not provided')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token is invalid')

        user_id = payload.get('user_id')
        user_email = payload.get('user_email')
		
        try:
            user = User.objects.get(id=user_id, email=user_email)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise AuthenticationFailed('User account is disabled')

        return (user_id, None)


class HasRequiredPermissions(BasePermission):
    message = 'You do not have permission to access this resource.'

    def has_permission(self, request, view):
        token = request.data.get('token')
        if not token:
            return False
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            permissions = payload.get('user_permissions')
            required_permissions = view.required_permissions
            return all(permission in permissions for permission in required_permissions)
        except (jwt.InvalidTokenError, AttributeError):
            return False