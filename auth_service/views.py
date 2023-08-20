from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from auth_service.authentication import TokenAuthentication
from auth_service.models import ExternAuthUser
from auth_service.parsers import EncryptJSONParser
from auth_service.permissions import CheckTokenForAllMicroservices
from auth_service.renderers import EncryptJSONRenderer
from auth_service.serializers import (
    LoginOrRegistrateUserByExternServiceSerializer,
    LoginUserSerializer,
    RegistrateUserSerializer,
)
from auth_service.utils import get_hash


class LoginUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckTokenForAllMicroservices]
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Авторизация пользователя"""
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = authenticate(request, username=data['username'], password=data['password'])
        if not user:
            return Response(status=status.HTTP_200_OK, data={'success': False})

        responsed_data = {
            'success': True,
            'microservice_auth_id': user.microservice_auth_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
        return Response(status=status.HTTP_200_OK, data=responsed_data)


class RegistrateUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckTokenForAllMicroservices]
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Регистрация пользователя"""
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_model = get_user_model()
        user = user_model.objects.filter(
            Q(username=data['username']) | Q(email=data['email']),
        ).first()
        if user:
            return Response(status=status.HTTP_200_OK, data={'success': False})

        user = user_model.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
        )
        responsed_data = {'success': True, 'microservice_auth_id': user.microservice_auth_id}
        return Response(status=status.HTTP_200_OK, data=responsed_data)


class LoginOrRegistrateUserByExternServiceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckTokenForAllMicroservices]
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def post(self, request):
        """Авторизация либо регистрация пользователя через внешний сервис"""
        serializer = LoginOrRegistrateUserByExternServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        extern_id = get_hash(data['extern_id'])
        extern_user = ExternAuthUser.objects.filter(extern_id=extern_id).first()
        if extern_user:
            user = extern_user.user
        else:
            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password='',
            )
            ExternAuthUser(user=user, extern_id=extern_id).save()

        responsed_data = {
            'success': True,
            'microservice_auth_id': user.microservice_auth_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'username': user.username,
        }
        return Response(status=status.HTTP_200_OK, data=responsed_data)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckTokenForAllMicroservices]
    parser_classes = [EncryptJSONParser]
    renderer_classes = [EncryptJSONRenderer]

    def get(self, request):
        """Отдача данных о пользователе"""

    def put(self, request):
        """Редактирование данных о пользователе"""

    def delete(self, request):
        """Удаление пользователя"""
