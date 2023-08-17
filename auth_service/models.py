import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class AuthUser(AbstractUser):
    microservice_auth_id = models.UUIDField(
        'Глобальный ID пользователя', null=False, blank=False, unique=True,
    )

    def make_microservice_auth_id(self):
        self.microservice_auth_id = uuid.uuid4()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ExternGoogleUser(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, on_delete=models.CASCADE, primary_key=True)
    extern_id = models.CharField(null=False, blank=False, unique=True, max_length=128)
