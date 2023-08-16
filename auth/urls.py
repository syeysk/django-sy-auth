from django.urls import path

from auth.views import (
    LoginUser,
    RegistrateUser,
    LoginOrRegistrateUserByExternService,
    ChangeUser,
)


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login_user'),
    path('registrate/', RegistrateUser.as_view(), name='registrate_user'),
    path(
        'login_or_registrate_by_extern/',
        LoginOrRegistrateUserByExternService.as_view(),
        name='login_or_registrate_by_extern',
    ),
    path('change/', ChangeUser.as_view(), name='change_user'),
]
