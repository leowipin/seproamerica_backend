from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import OperationalStaff, AdministrativeStaff, Charge

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'dni')

    def create(self, validated_data, group_name):
        group = Group.objects.get(name=group_name)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.groups.add(group)
        #user.user_permissions.set(group.permissions.all())
        return user
    def save(self):
        validated_data = self.validated_data
        group_name = self.context['group_name']
        return self.create(validated_data, group_name)


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, queryset=Permission.objects.all(), slug_field='codename', write_only=True)
    
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class ChargeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Charge
        fields = '__all__'    
        
class AdminStaffSerializer(serializers.ModelSerializer):
    charge = serializers.SlugRelatedField(queryset=Charge.objects.all(), slug_field='name', write_only=True)

    class Meta:
        model = AdministrativeStaff
        fields = ('branch', 'charge', 'user')