from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from rest_framework.views import APIView

from django_postcode_lookup import loading, serializers


class PostcodeLookupView(APIView):
    authentication_classes = ()
    serializer_class = serializers.PostcodeLookupSerializer
    backend = loading.get_backend()

    def post(self, request, format=None):
        """
        Usage::

            POST /checkout/address-lookup
            {
                'postcode': X,
                'number': Y,
                'key': 'signing-key',
            }

        Returns::

            {
              "data": {
                "city": "UTRECHT",
                "street": "Ravellaan",
                "number": "16,
                "postcode": "3533JN",
              }
            }


        """
        if not self.backend:
            raise ImproperlyConfigured("No backend is defined")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.backend.lookup(
            postcode=serializer.data['postcode'],
            number=serializer.data['number'])
        return Response(result.json())

    def get_serializer(self, **kwargs):
        return self.serializer_class(
            backend=self.backend, **kwargs)
