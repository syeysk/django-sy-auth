from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegistrateUserSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("A password must have length more 10 symbols")

        return value

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class LoginOrRegistrateUserByExternServiceSerializerOld(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    extern_id = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'extern_id']


class LoginOrRegistrateUserByExternServiceGoogleSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=150)


class LoginOrRegistrateUserByExternServiceSerializer(serializers.Serializer):
    extern_service = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=150)
    extern_token = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=150)

    def validate(self, data):
        if data['extern_service'] == 'google':
            serializer = LoginOrRegistrateUserByExternServiceGoogleSerializer(data=data['extra'])
            serializer.is_valid(raise_exception=True)
            data['extra'] = serializer.validated_data

        return data


class UserPutSerializer(serializers.ModelSerializer):
    current_username = serializers.CharField(max_length=150, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['current_username', 'username', 'first_name', 'last_name']
