from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.parsers import JSONParser
from rest_framework import authentication

from auth_service.utils import decrypt_request_body


class TempTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        parser_context = {'request': request}
        json_data = JSONParser().parse(
            stream=request.stream,
            media_type='application/json',
            parser_context=parser_context,
        )
        decrypted_data = decrypt_request_body(json_data, request)
        user = get_user_model().objects.filter(microservice_auth_id=decrypted_data['microservice_auth_id']).first()
        request.decrypted_data = decrypted_data
        return user or AnonymousUser, decrypted_data.pop('token')
