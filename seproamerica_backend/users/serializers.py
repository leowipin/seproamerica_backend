from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import OperationalStaff, AdministrativeStaff

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'dni')

    def create(self, validated_data):
        group = Group.objects.get(name='client')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.groups.add(group)
        #user.user_permissions.set(group.permissions.all())
        user.save()
        return user
