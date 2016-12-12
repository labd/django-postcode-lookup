from rest_framework import serializers


class PostcodeLookupSerializer(serializers.Serializer):
    postcode = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
