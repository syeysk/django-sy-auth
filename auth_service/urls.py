from django.urls import path

from auth_service.views import (
    LoginUserView,
    RegistrateUserView,
    LoginOrRegistrateUserByExternServiceView,
    UserView,
)


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('registrate/', RegistrateUserView.as_view(), name='registrate_user'),
    path(
        'login_or_registrate_by_extern/',
        LoginOrRegistrateUserByExternServiceView.as_view(),
        name='login_or_registrate_by_extern',
    ),
    path('user/', UserView.as_view(), name='user'),
]
