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

        responsed_data = {'user_id': 'test', 'last_name': 'test lname', 'first_name': 'test fname'}
        return Response(status=status.HTTP_200_OK, data=responsed_data)


class RegistrateUserView(APIView):
    def post(self, request):
        """Регистрация пользователя"""
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        responsed_data = {'user_id': 'test'}
        return Response(status=status.HTTP_200_OK, data=responsed_data)


class LoginOrRegistrateUserByExternServiceView(APIView):
    def post(self, request):
        """Авторизация либо регистрация пользователя через внешний сервис"""


class ChangeUserView(APIView):
    def put(self, request):
        """Редактирование данных о пользователе"""

    def delete(self, request):
        """Удаление пользователя"""
