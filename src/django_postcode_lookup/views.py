from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from rest_framework.views import APIView

from django_postcode_lookup import loading, serializers


class PostcodeLookupView(APIView):
    authentication_classes = ()
    serializer_class = serializers.PostcodeLookupSerializer
    backend = loading.get_backend()

    def get(self, request, format=None):
        """
        Usage::

            GET /checkout/address-lookup?postcode=X&number=Y

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

        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = self.backend.lookup(**serializer.data)
        return Response(result.json())
