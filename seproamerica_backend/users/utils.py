import jwt
from django.contrib.auth.models import Permission
from seproamerica_backend import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .models import ImagenesPerfil
from datetime import datetime, timedelta
from firebase_admin import storage
import base64
from io import BytesIO

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

def upload_img(user_id, user, request, url_img, img_modified):
    if 'id' in request.data:
        if not user.is_admin:
            return Response({'message': 'No tienes permiso para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('id')
    if url_img is not None:
        # Obtener la instancia de ImagenesPerfil asociada a ese usuario
        try:
            imagen_perfil = ImagenesPerfil.objects.get(user_id=user_id)
        except ImagenesPerfil.DoesNotExist:
            imagen_perfil = None
        # Verificar si la url_img enviada en el request ya está asociada a ese usuario
        if imagen_perfil is None or imagen_perfil.url_img != url_img:
            components = url_img.split(',')
            image_base64 = components[1]
            if 'jpeg' in components[0] or 'jpg' in components[0]:
                content_type = 'image/jpeg'
            elif 'png' in components[0]:
                content_type = 'image/png'
            else:
                return Response({'error': 'Formato de imagen no válido'}, status=status.HTTP_400_BAD_REQUEST)
            # Decodificar la imagen en base64 y convertirla en un objeto BytesIO
            image_data = base64.b64decode(image_base64)
            image = BytesIO(image_data)
            # Subir la imagen a Firebase Storage y obtener la URL de descarga
            bucket = storage.bucket('seproamerica-858ec.appspot.com')
            blob = bucket.blob(f'profilePictures/{user_id}')
            blob.upload_from_file(image, content_type=content_type)
            expiration = datetime.utcnow() + timedelta(days=365*20)
            download_url = blob.generate_signed_url(expiration=expiration, method='GET')
            img_modified = True
            # Guardar la URL de descarga en el modelo ImagenesPerfil
            ImagenesPerfil.objects.update_or_create(
                user_id=user_id,
                defaults={'url_img': download_url}
            )
    return img_modified    
    