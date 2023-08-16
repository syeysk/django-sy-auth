from rest_framework.views import APIView


class LoginUser(APIView):
    def post(self, request):
        """Авторизация пользователя"""


class RegistrateUser(APIView):
    def post(self, request):
        """Регистрация пользователя"""


class LoginOrRegistrateUserByExternService(APIView):
    def post(self, request):
        """Авторизация либо регистрация пользователя через внешний сервис"""


class ChangeUser(APIView):
    def put(self, request):
        """Редактирование данных о пользователе"""

    def delete(self, request):
        """Удаление пользователя"""
