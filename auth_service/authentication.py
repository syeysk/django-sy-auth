import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.parsers import JSONParser
from rest_framework import authentication

from auth_service.utils import decrypt, load_private_key


class TempTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        with open('private_key', 'rb') as file_private_key:
            private_key = load_private_key(file_private_key.read())

        parser_context = {'request': request}
        json_data = JSONParser().parse(
            stream=request.stream,
            media_type='application/json',
            parser_context=parser_context,
        )
        decrypted_json = decrypt(json_data['data'], private_key)
        print('INPUT:', decrypted_json)
        request.decrypted_data = json.loads(decrypted_json)
        token = request.decrypted_data['token']
        user = get_user_model().objects.filter(
            microservice_auth_id=request.decrypted_data['microservice_auth_id'],
        ).first()
        return user or AnonymousUser, token
