import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from auth_service.authentication import TempTokenAuthentication
from auth_service.models import DeletedUsers, ExternAuthUser, TempToken
from auth_service.parsers import EncryptJSONParser, TempTokenEncryptJSONParser
from auth_service.permissions import CheckTempToken
from auth_service.renderers import EncryptJSONRenderer
from auth_service.serializers import (
    LoginOrRegistrateUserByExternServiceSerializer,
    LoginOrRegistrateUserByExternServiceSerializerOld,
    LoginUserSerializer,
    LoginUserByEmailSerializer,
    RegistrateUserSerializer,
    UserPutSerializer,
    SearchUserSerializer,
    RequiredParamsMixin,
)
from auth_service.serializers_response import (
    PublicKeyViewSerializer,
)
from auth_service.utils import generate_keys, get_hash


parameter_microservice_auth_id = OpenApiParameter(
    name='microservice_auth_id',
    description='Глобальный идентификатор пользователя',
    required=True,
    type=str,
)


@extend_schema(
    tags=['1. Ключи'],
    responses={200: PublicKeyViewSerializer},
    summary='Получение открытого ключа для шифрования последующих запросов',
)
class PublicKeyView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        import os.path
        if os.path.exists('public_key'):
            with open('public_key', 'rb') as file_public_key:
                public_key = file_public_key.read()
        else:
            private_key, public_key = generate_keys()
            with open('public_key', 'wb') as file_public_key:
                file_public_key.write(public_key)

            with open('private_key', 'wb') as file_private_key:
                file_private_key.write(private_key)

        return Response(status=status.HTTP_200_OK, data={'public_key': public_key})


@extend_schema(
    tags=['2. Временный токен'],
    request=LoginUserSerializer,
    summary='Авторизовать пользователя через логин/пароль (нерекомендуемый метод, будет удалён в следующих версиях)',
)
class LoginUserView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Авторизация пользователя"""
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = authenticate(request, username=data['username'], password=data['password'])
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'password': ['неверный логин или пароль']})

        token, _ = TempToken.objects.create_token(user.microservice_auth_id)
        response_data = {
            'microservice_auth_id': user.microservice_auth_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'token': token,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


@extend_schema(
    tags=['2. Временный токен'],
    request=LoginUserByEmailSerializer,
    summary='Авторизовать пользователя через электронную почту и пароль',
)
class LoginUserByEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Авторизация пользователя"""
        serializer = LoginUserByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = authenticate(request, username=data['email'], password=data['password'])
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'password': ['неверная почта или пароль']})

        token, _ = TempToken.objects.create_token(user.microservice_auth_id)
        response_data = {
            'microservice_auth_id': user.microservice_auth_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'token': token,
            'username': user.username,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


@extend_schema(
    tags=['2. Временный токен'],
    request=RegistrateUserSerializer,
    summary='Зарегистрировать и затем авторизовать пользователя ',
)
class RegistrateUserView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Регистрация пользователя"""
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_model = get_user_model()
        user = user_model.objects.filter(email=data['email']).first()
        if user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'username': ['Пользователь с таким email уже существует']},
            )

        user = user_model.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
        )
        token, _ = TempToken.objects.create_token(user.microservice_auth_id)
        response_data = {'microservice_auth_id': user.microservice_auth_id, 'token': token}
        return Response(status=status.HTTP_200_OK, data=response_data)


@extend_schema(
    tags=['2. Временный токен'],
    parameters=[
        OpenApiParameter(
            name='old_token',
            description='Токен старого типа. Это единственный токен, выдаваемый администратором вручную.',
            required=True,
            type=str,
        ),
    ],
    request=LoginOrRegistrateUserByExternServiceSerializer,
    summary='Авторизовать пользователя через Google',
)
class LoginOrRegistrateUserByExternServiceView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Авторизация либо регистрация пользователя через внешний сервис"""
        old_token = request.data.get('old_token')
        if old_token:
            if old_token not in set(settings.MICROSERVICES_TOKENS.values()):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'old_token': [
                            (
                                'не указан устаревший токен. Для получения старого токена, пожалуйста, обратитесь'
                                ' к администратору микроcервиса авторизации'
                            )
                        ],
                    },
                )

            serializer = LoginOrRegistrateUserByExternServiceSerializerOld(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.validated_data
        else:
            serializer = LoginOrRegistrateUserByExternServiceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            extern_service = data['extern_service']
            if data['extern_service'] == 'google':
                params = {
                    'access_token': data['extern_token'],
                    'id_token': data['extra']['id_token'],
                    'token_type': 'Bearer',
                    'expires_in': 3599,
                }
                response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params=params)
                user_info = response.json()
                if not user_info['verified_email']:
                    response_data = {'message': 'E-mail в учётной записи Google не подтверждён. Пожалуйста, подтвердите e-mail и попробуйте авторизоваться вновь.'}
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=response_data)

                user_data = {
                    'username': user_info['email'].split('@')[0],
                    'email': user_info['email'],
                    'first_name': user_info.get('given_name', ''),
                    'last_name': user_info.get('family_name', ''),
                    'extern_id': '{}-{}'.format(extern_service, user_info['id']),
                }
            else:
                response_data = {'message': 'Invalid "extern_service"'}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response_data)

        extern_id = get_hash(user_data['extern_id'])
        extern_user = ExternAuthUser.objects.filter(extern_id=extern_id).first()
        if extern_user:
            user = extern_user.user
        else:
            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password='',
            )
            ExternAuthUser(user=user, extern_id=extern_id).save()

        token, _ = TempToken.objects.create_token(user.microservice_auth_id)
        response_data = {
            'microservice_auth_id': user.microservice_auth_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'username': user.username,
            'token': token,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class UserView(APIView):
    authentication_classes = [TempTokenAuthentication]
    permission_classes = [CheckTempToken]
    parser_classes = [TempTokenEncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    @extend_schema(
        tags=['3. Пользователь'],
        request=RequiredParamsMixin,
        summary='Получить данные пользователя',
    )
    def get(self, request):
        """Отдача данных о пользователе"""
        user = request.user
        response_data = {
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'email': user.email,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    @extend_schema(
        tags=['3. Пользователь'],
        parameters=[
            parameter_microservice_auth_id,
        ],
        request=type('UserPutSerializerWithMixin', (RequiredParamsMixin, UserPutSerializer), {}),
        # request=UserPutSerializer,
        summary='Изменить данные пользователя',
    )
    def put(self, request):
        """Редактирование данных о пользователе"""
        instance = request.user
        serializer = UserPutSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_fields = [
            name for name, value in serializer.validated_data.items()
            if name != 'current_username' and getattr(instance, name) != value
        ]
        serializer.save()
        response_data = {
            'updated_fields': updated_fields,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    @extend_schema(
        tags=['3. Пользователь'],
        parameters=[
            parameter_microservice_auth_id,
        ],
        summary='Удалить пользователя',
    )
    def delete(self, request):
        """Удаление пользователя"""
        user = request.user
        DeletedUsers(microservice_auth_id=user.microservice_auth_id).save()
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return Response(status=status.HTTP_200_OK, data={})


class SearchUserView(APIView):
    authentication_classes = [TempTokenAuthentication]
    permission_classes = [CheckTempToken]
    parser_classes = [TempTokenEncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    @extend_schema(
        tags=['4. Прочие методы'],
        parameters=[
            parameter_microservice_auth_id,
        ],
        request=SearchUserSerializer,
        summary='Поиск пользователя',
    )
    def post(self, request):
        serializer = SearchUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        search_string = serializer.validated_data['search_string']
        query = (
                    Q(username__contains=search_string)
                    | Q(last_name__contains=search_string)
                    | Q(first_name__contains=search_string)
                    | Q(email__contains=search_string)
        )
        users_data = get_user_model().objects.filter(query).values('username', 'last_name', 'first_name')[:5]
        return Response(status=status.HTTP_200_OK, data={'users_data': list(users_data)})
