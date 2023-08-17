import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


def make_microservice_auth_id():
    return uuid.uuid4()


class AuthUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        extra_fields['microservice_auth_id'] = make_microservice_auth_id()
        return super()._create_user(username, email, password, **extra_fields)


class AuthUser(AbstractUser):
    microservice_auth_id = models.UUIDField(
        'Глобальный ID пользователя', null=False, blank=False, unique=True,
    )

    objects = AuthUserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ExternGoogleUser(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, on_delete=models.CASCADE, primary_key=True)
    extern_id = models.CharField(null=False, blank=False, unique=True, max_length=128)
