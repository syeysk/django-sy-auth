from rest_framework.renderers import JSONRenderer

from auth_service.utils import encrypt_text


class EncryptJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = super().render(data, accepted_media_type, renderer_context)
        data = {'data': encrypt_text(data.decode())}
        return super().render(data, accepted_media_type, renderer_context)
