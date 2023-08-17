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
