from rest_framework.permissions import BasePermission


class CheckTokenForAllMicroservices(BasePermission):
    def has_permission(self, request, view):
        return request.auth == request.auth  # TODO: реализовать
