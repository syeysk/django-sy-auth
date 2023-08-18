from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication


class TokenAuthentication(authentication.BaseAuthentication):
    TOKEN_TYPE = 'Token'

    def authenticate(self, request):
        type_and_token_str = request.META.get('HTTP_AUTHORIZATION')
        if type_and_token_str:
            type_and_token = type_and_token_str.split()
            if len(type_and_token) == 2:
                if type_and_token[0] == self.TOKEN_TYPE:
                    return AnonymousUser, type_and_token[1]

    def authenticate_header(self, request):
        return self.TOKEN_TYPE
