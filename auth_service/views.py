from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from auth_service.serializers import LoginUserSerializer, RegistrateUserSerializer


class LoginUserView(APIView):
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

        # user = user_model(
        #     username=data['username'],
        #     email=data['email'],
        #     first_name=data['first_name'],
        #     last_name=data['last_name'],
        # )
        # user.set_password(data['password'])
        # user.make_microservice_auth_id()
        # user.save()

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
    def post(self, request):
        """Авторизация либо регистрация пользователя через внешний сервис"""


class ChangeUserView(APIView):
    def put(self, request):
        """Редактирование данных о пользователе"""

    def delete(self, request):
        """Удаление пользователя"""
