from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_service.models import AuthUser


admin.site.register(AuthUser, UserAdmin)
