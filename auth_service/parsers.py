import json

from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from auth_service.utils import decrypt_text


class EncryptJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        json_data = super().parse(stream, media_type, parser_context)
        try:
            return json.loads(decrypt_text(json_data['data']))
        except Exception as exc:
            raise ParseError('Encrypted JSON parse error - %s' % str(exc))
