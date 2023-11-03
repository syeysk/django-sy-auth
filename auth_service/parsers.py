import json

from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from auth_service.utils import decrypt, load_private_key, load_public_key


class EncryptJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        request = parser_context['request']
        json_data = super().parse(stream, media_type, parser_context)
        with open('private_key', 'rb') as file_private_key:
            private_key = load_private_key(file_private_key.read())

        decrypted_json = decrypt(json_data['data'], private_key)
        try:
            decrypted_data = json.loads(decrypted_json)
            del decrypted_data['random_trash']
            request.public_key = load_public_key(decrypted_data.pop('public_key').encode())
            print('INPUT:', decrypted_data)
            return decrypted_data
        except Exception as exc:
            raise ParseError('Encrypted JSON parse error - %s' % str(exc))


class TempTokenEncryptJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        request = parser_context['request']
        try:
            decrypted_data = request.decrypted_data
            del decrypted_data['random_trash']
            request.public_key = load_public_key(decrypted_data.pop('public_key').encode())
            return decrypted_data
        except Exception as exc:
            raise ParseError('Encrypted JSON parse error - %s' % str(exc))
