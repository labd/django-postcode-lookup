from django.core.exceptions import ValidationError
from rest_framework import serializers


class PostcodeLookupSerializer(serializers.Serializer):
    postcode = serializers.CharField(required=True)
    number = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        backend = kwargs.pop('backend')
        super(PostcodeLookupSerializer, self).__init__(*args, **kwargs)
