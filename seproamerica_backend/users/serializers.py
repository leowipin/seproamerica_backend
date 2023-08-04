from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import PersonalOperativo, PersonalAdministrativo, Cargo, Cliente, Sucursal, Usuario, CuentaTelefono, Empresa, ImagenesPerfil

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'dni', 'gender', 'address', 'birthdate')

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
            raise serializers.ValidationError('Correo o contraseña incorrectos')
        return user
    
class SignInPhoneAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Correo o contraseña incorrectos')

        if user.password != password:
            raise serializers.ValidationError('Correo o contraseña incorrectos')

        return user
# serializer needed to manage the data that an admin can modify of a personal    
class AdminPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password', 'first_name', 'last_name', 'phone_number', 'dni', 'birthdate', 'gender', 'address', 'isVerified', 'is_active', 'date_joined')

class OperationalPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'dni', 'birthdate', 'gender', 'address', 'isVerified', 'is_active', 'date_joined')
# serializer needed to manage the data that an admin can modify of a client
class ClientPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('isVerified', 'is_active')

# serializer needed to manage the data that a client can modify about himself
class ClientUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    url_img = serializers.CharField(source='imagenesperfil.url_img', read_only=True)
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'dni', 'phone_number', 'birthdate', 'address', 'gender', 'email', 'url_img')
    

class ClientNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Usuario
        fields = ('first_name', 'last_name')

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenesPerfil
        fields = '__all__'

class PhoneNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Usuario
        fields = ('first_name',)

class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'is_admin')

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, queryset=Permission.objects.all(), slug_field='name')

    class Meta:
        model = Group
        fields = ('id','name', 'permissions')

class PhoneUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['email', 'password']

    def create(self, validated_data, group_name):
        user = User.objects.create(**validated_data)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return user
    
    def save(self):
        validated_data = self.validated_data
        group_name = self.context['group_name']
        return self.create(validated_data, group_name)
    
class PhoneInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['id' ,'email', 'first_name', 'password', 'is_active']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

class PhoneAccountSerializer(serializers.ModelSerializer):
     class Meta:
        model = CuentaTelefono
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')

class StaffSerializer(serializers.ModelSerializer):
    charge = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'is_admin', 'charge')
    
    def get_charge(self, obj):
        return obj.personaloperativo.charge.name

class ChargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = ['id', 'name', 'description', 'type']    
    

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sucursal
        fields = '__all__'    


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    dni = serializers.CharField(source='user.dni')
    url_img = serializers.CharField(source='user.imagenesperfil.url_img')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    isVerified = serializers.BooleanField(source='user.isVerified')
    is_active = serializers.BooleanField(source='user.is_active')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    group = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name', source='user.groups.first')

    class Meta:
        model = Cliente
        fields = ('id', 'first_name', 'last_name', 'email', 'dni', 'url_img', 'birthdate', 'gender', 'address', 'phone_number', 'isVerified', 'is_active', 'date_joined', 'group')


class ClientSignUpSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = Cliente
        fields = '__all__'

        
class AdminStaffSerializer(serializers.ModelSerializer):
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name', write_only=True)
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name', write_only=True)

    class Meta:
        model = PersonalAdministrativo
        fields = ('branch', 'charge', 'user', 'start_date', 'final_date')


class AdminInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    dni = serializers.CharField(source='user.dni')
    url_img = serializers.CharField(source='user.imagenesperfil.url_img')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    is_active = serializers.BooleanField(source='user.is_active')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name')
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name')
    group = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name', source='user.groups.first')
    #created_by = serializers.SlugRelatedField(queryset=Usuario.objects.all(), slug_field='email')

    class Meta:
        model = PersonalAdministrativo
        fields = ('id','first_name', 'last_name', 'email', 'dni', 'url_img', 'birthdate', 'gender', 'address', 'phone_number', 'is_active', 'date_joined', 'start_date', 'final_date', 'charge', 'branch','group')


class OperationalStaffSerializer(serializers.ModelSerializer):
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name', write_only=True)
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name', write_only=True)

    class Meta:
        model = PersonalOperativo
        fields = ('branch', 'charge', 'user', 'created_by', 'start_date', 'final_date')

class OperationalInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    dni = serializers.CharField(source='user.dni')
    url_img = serializers.CharField(source='user.imagenesperfil.url_img')
    birthdate = serializers.DateField(source='user.birthdate')
    gender = serializers.CharField(source='user.gender')
    address = serializers.CharField(source='user.address')
    phone_number = serializers.CharField(source='user.phone_number')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    charge = serializers.SlugRelatedField(queryset=Cargo.objects.all(), slug_field='name')
    branch = serializers.SlugRelatedField(queryset=Sucursal.objects.all(), slug_field='name')
    created_by = serializers.SlugRelatedField(queryset=Usuario.objects.all(), slug_field='email')

    class Meta:
        model = PersonalOperativo
        fields = ('id','first_name', 'last_name', 'email', 'dni', 'birthdate', 'url_img', 'gender', 'address', 'phone_number', 'date_joined', 'start_date', 'final_date', 'charge', 'branch', 'created_by')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'