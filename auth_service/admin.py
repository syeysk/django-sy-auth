from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_service.models import AuthUser, ExternAuthUser


admin.site.register(AuthUser, UserAdmin)


class ExternAuthUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExternAuthUser, ExternAuthUserAdmin)
