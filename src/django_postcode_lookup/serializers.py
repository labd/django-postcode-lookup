from rest_framework import serializers
from django_postcode_lookup import signing
from django.core.exceptions import ValidationError


class PostcodeLookupSerializer(serializers.Serializer):
    postcode = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
    key = serializers.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        backend = kwargs.pop('backend')

        super(PostcodeLookupSerializer, self).__init__(*args, **kwargs)
        if not backend.validate_api_key:
            self.fields.pop('key')

    def validate_key(self, value):
        try:
            signing.validate_api_key(value)
        except signing.SignatureExpired:
            raise ValidationError("Invalid/expired key")
        return value
