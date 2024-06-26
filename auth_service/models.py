import datetime
import uuid
from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from auth_service.validators import UnicodeUsernameValidator

from auth_service.utils import get_hash


def make_microservice_auth_id():
    return uuid.uuid4()


class AuthUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        extra_fields['microservice_auth_id'] = make_microservice_auth_id()
        return super()._create_user(username, email, password, **extra_fields)


class TempTokenManager(models.Manager):
    TOKEN_SIZE = 16
    EXPIRE_DAYS = 1

    def create_token(self, microservice_auth_id, **extra_fields):
        token = token_urlsafe(16)
        token_obj = self.model(**extra_fields)
        token_obj.token = get_hash(f'{token}{microservice_auth_id}', self.TOKEN_SIZE)
        token_obj.save(using=self._db)
        return token, token_obj

    def authenticate(self, microservice_auth_id, token):
        start_expire_dt = datetime.datetime.today() - datetime.timedelta(days=self.EXPIRE_DAYS)
        return self.filter(
            token=get_hash(f'{token}{microservice_auth_id}', self.TOKEN_SIZE),
            dt_create__gte=start_expire_dt,
        ).first()


class AuthUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.'),
        validators=[username_validator],
    )
    microservice_auth_id = models.UUIDField(
        'Глобальный ID пользователя', null=False, blank=False, unique=True,
    )

    objects = AuthUserManager()

    class Meta(AbstractUser.Meta):
        indexes = [
            models.Index(fields=['username'], name='auth_user_username'),
            models.Index(fields=['first_name'], name='auth_user_first_name'),
            models.Index(fields=['last_name'], name='auth_user_last_name'),
            models.Index(fields=['email'], name='auth_user_email'),
        ]
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


class TempToken(models.Model):
    token = models.CharField(max_length=32)
    dt_create = models.DateTimeField(auto_now_add=True)

    objects = TempTokenManager()
