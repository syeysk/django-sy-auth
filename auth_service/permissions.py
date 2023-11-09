from rest_framework.permissions import BasePermission

from auth_service.models import TempToken


class CheckTempToken(BasePermission):
    def has_permission(self, request, view):
        return (
            not request.user.is_anonymous
            and TempToken.objects.authenticate(request.user.microservice_auth_id, request.auth)
        )
