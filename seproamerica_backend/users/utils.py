import jwt
from django.contrib.auth.models import Permission
from seproamerica_backend import settings
from rest_framework.exceptions import AuthenticationFailed

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

def get_token(request):

    header = request.META.get('HTTP_AUTHORIZATION')

    if not header:
        raise AuthenticationFailed('Token not provided')
        
    parts = header.split()
    if parts[0].lower() != 'bearer':
        raise AuthenticationFailed('Invalid authentication scheme')

    if len(parts) == 1:
        raise AuthenticationFailed('Token not provided')

    if len(parts) > 2:
        raise AuthenticationFailed('Invalid Authorization header')
        
    token = parts[1]

    return token

def perms_englishtospanish(codename):
    if "view" in codename:
        codename = codename.replace("view","ver")
    if "add" in codename:
        codename = codename.replace("add","crear")
    if "change" in codename:
        codename = codename.replace("change","modificar")
    if "delete" in codename:
        codename = codename.replace("delete","eliminar")
    return codename

def perms_spanishtoenglish(codename):
    if "ver" in codename:
        codename = codename.replace("ver", "view")
    if "crear" in codename:
        codename = codename.replace("crear", "add")
    if "modificar" in codename:
        codename = codename.replace("modificar", "change")
    if "eliminar" in codename:
        codename = codename.replace("eliminar", "delete")
    return codename