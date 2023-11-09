from secrets import token_urlsafe
from random import randint

from rest_framework.renderers import JSONRenderer

from auth_service.utils import encrypt


class EncryptJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context['request']
        with open('public_key', 'rb') as file_public_key:
            auth_public_key = file_public_key.read()

        data['random_trash'] = token_urlsafe(randint(5, 20))
        data['public_key'] = auth_public_key
        data = super().render(data, accepted_media_type, renderer_context)
        encrypted_data = encrypt(data, request.public_key)
        data = {'data': encrypted_data}
        return super().render(data, accepted_media_type, renderer_context)
