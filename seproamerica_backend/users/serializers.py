from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import PersonalOperativo, PersonalAdministrativo, Cargo, Cliente, Sucursal, Usuario

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
        return user
    def save(self):
        validated_data = self.validated_data
        group_name = self.context['group_name']
        return self.create(validated_data, group_name)

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Incorrect credentials')
        return user

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, queryset=Permission.objects.all(), slug_field='codename')

    class Meta:
        model = Group
        fields = ('name', 'permissions')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')


class ChargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = '__all__'    
    

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sucursal
        fields = '__all__'    


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    dni = serializers.CharField(source='user.dni')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    isVerified = serializers.BooleanField(source='user.isVerified')
    date_joined = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = Cliente
        fields = ('id', 'email', 'username', 'dni', 'birthdate', 'gender', 'address', 'phone_number', 'isVerified', 'date_joined')

        
class AdminStaffSerializer(serializers.ModelSerializer):
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name', write_only=True)
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name', write_only=True)

    class Meta:
        model = PersonalAdministrativo
        fields = ('branch', 'charge', 'user')


class AdminInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    dni = serializers.CharField(source='user.dni')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    isVerified = serializers.BooleanField(source='user.isVerified')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name')
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name')
    #created_by = serializers.SlugRelatedField(queryset=Usuario.objects.all(), slug_field='email')

    class Meta:
        model = PersonalAdministrativo
        fields = ('id', 'email', 'username', 'dni', 'birthdate', 'gender', 'address', 'phone_number', 'isVerified', 'date_joined', 'start_date', 'final_date', 'charge', 'status', 'branch')


class OperationalStaffSerializer(serializers.ModelSerializer):
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name', write_only=True)
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name', write_only=True)

    class Meta:
        model = PersonalOperativo
        fields = ('branch', 'charge', 'user', 'created_by')

class OperationalInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    dni = serializers.CharField(source='user.dni')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    isVerified = serializers.BooleanField(source='user.isVerified')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name')
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name')
    created_by = serializers.SlugRelatedField(queryset=Usuario.objects.all(), slug_field='email')

    class Meta:
        model = PersonalOperativo
        fields = ('id', 'email', 'username', 'dni', 'birthdate', 'gender', 'address', 'phone_number', 'isVerified', 'date_joined', 'start_date', 'final_date', 'charge', 'status', 'branch', 'created_by')