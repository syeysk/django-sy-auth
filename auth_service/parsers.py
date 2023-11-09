from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from auth_service.utils import decrypt_request_body


class EncryptJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        request = parser_context['request']
        json_data = super().parse(stream, media_type, parser_context)
        try:
            return decrypt_request_body(json_data, request)
        except Exception as exc:
            raise ParseError('Encrypted JSON parse error - %s' % str(exc))


class TempTokenEncryptJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        return parser_context['request'].decrypted_data
