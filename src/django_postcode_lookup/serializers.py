from rest_framework import serializers


class PostcodeLookupSerializer(serializers.Serializer):
    postcode = serializers.CharField(required=True)
    number = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop('backend')
        super(PostcodeLookupSerializer, self).__init__(*args, **kwargs)
