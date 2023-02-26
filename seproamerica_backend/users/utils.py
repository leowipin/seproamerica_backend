import jwt
from django.contrib.auth.models import Permission
from seproamerica_backend import settings

def generate_token(user):
    group = user.groups.first()
    permissions = Permission.objects.filter(group=group)
    permission_names = [p.codename for p in permissions]

    payload = {
        "user_id": user.id,
        "user_email": user.email,
        "user_permissions": permission_names,
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    return token