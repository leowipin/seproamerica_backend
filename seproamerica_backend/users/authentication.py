import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from seproamerica_backend import settings
from django.contrib.auth import get_user_model
from users.utils import get_token

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        token = get_token(request)

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
        
        token = get_token(request)
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            permissions = payload.get('user_permissions')
            required_permissions = view.required_permissions
            return all(permission in permissions for permission in required_permissions)
        except (jwt.InvalidTokenError, AttributeError):
            return False