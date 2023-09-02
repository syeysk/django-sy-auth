from django.conf import settings
from rest_framework.permissions import BasePermission


class CheckTokenForAllMicroservices(BasePermission):
    def has_permission(self, request, view):
        return request.auth in set(settings.MICROSERVICES_TOKENS.values())  # TODO: реализовать нормально!
