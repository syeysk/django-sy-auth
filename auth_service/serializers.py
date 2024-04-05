from django.contrib.auth import get_user_model
from rest_framework import serializers


class RequiredParamsMixin(serializers.Serializer):
    microservice_auth_id = serializers.UUIDField(
        help_text='Глобальный идентификатор пользователя',
        allow_null=False,
        required=True,
    )


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class LoginUserByEmailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


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
    id_token = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=5000)


class LoginOrRegistrateUserByExternServiceSerializer(serializers.Serializer):
    extern_service = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=50)
    extern_token = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=500)
    extra = serializers.JSONField(required=True, allow_null=False)

    def validate(self, data):
        if data['extern_service'] == 'google':
            serializer = LoginOrRegistrateUserByExternServiceGoogleSerializer(data=data['extra'])
            serializer.is_valid(raise_exception=True)
            data['extra'] = serializer.validated_data

        return data


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']


class SearchUserSerializer(serializers.Serializer):
    search_string = serializers.CharField(
        help_text='Слово для поиска. Поиск происходит по имени пользователя, фамилии, имени и email',
        required=True,
        allow_null=False,
        allow_blank=True,
        max_length=20,
    )
