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


class ExternAuthUser(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, on_delete=models.CASCADE, primary_key=True)
    extern_id = models.CharField(null=False, blank=False, unique=True, max_length=128)


class DeletedUsers(models.Model):
    STEP_MARKED = 1
    STEP_DELETED = 2
    STEP_CHOICES = (
        ('marked', STEP_MARKED),
        ('deleted', STEP_DELETED),
    )
    dt_delete = models.DateTimeField(auto_now_add=True)
    microservice_auth_id = models.UUIDField(
        'Глобальный ID удалённого пользователя', null=False, blank=False, unique=True,
    )
    step = models.IntegerField(choices=STEP_CHOICES, default=STEP_MARKED)
