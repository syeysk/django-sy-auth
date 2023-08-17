from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegistrateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class LoginOrRegistrateUserByExternServiceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    extern_id = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'extern_id']
