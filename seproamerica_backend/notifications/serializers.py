from rest_framework import serializers
from .models import TokenFCM, OrderClientNotification, OrderAdminNotification

class TokenFCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenFCM
        fields = '__all__'


class OrderClientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClientNotification
        fields = '__all__'

class ClientInfoNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClientNotification
        fields = ('title', 'message', 'url_img', 'date_sended')

class OrderAdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAdminNotification
        fields = '__all__'