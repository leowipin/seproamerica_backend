import jwt
from django.contrib.auth.models import Permission
from seproamerica_backend import settings
from rest_framework.exceptions import AuthenticationFailed

def generate_token(user):

    payload = {
        "user_id": user.id,
        "user_email": user.email,
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

def perms_englishtospanish(name):
    name = name.replace("Can ", "puede ") 
    if "view" in name:
        name = name.replace(" view "," ver ")
    elif "add" in name:
        name = name.replace(" add "," crear ")
    elif "change" in name:
        name = name.replace(" change "," modificar ")
    elif "delete" in name:
        name = name.replace(" delete "," eliminar ")
    return name

def perms_spanishtoenglish(name):
    name = name.replace("puede ", "Can ")
    if "ver" in name:
        name = name.replace(" ver ", " view ")
    if "crear" in name:
        name = name.replace(" crear ", " add ")
    if "modificar" in name:
        name = name.replace(" modificar ", " change ")
    if "eliminar" in name:
        name = name.replace(" eliminar ", " delete ")
    return name