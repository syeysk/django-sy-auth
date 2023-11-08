from rest_framework import serializers


class PublicKeyViewSerializer(serializers.Serializer):
    public_key = serializers.CharField(
        max_length=150,
        help_text='Открытый ключ, которым необходимо шифровать все последующие запросы',
    )
