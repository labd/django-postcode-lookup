from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_postcode_lookup import loading, serializers
from django_postcode_lookup.backends.base import PostcodeLookupException


class PostcodeLookupView(APIView):
    authentication_classes = ()
    serializer_class = serializers.PostcodeLookupSerializer
    backend = loading.get_backend()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        """Add csrf validation to this endpoint without authentication."""
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Usage::

            POST /checkout/address-lookup
            {
                'postcode': X,
                'number': Y,
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

        try:
            result = self.backend.lookup(
                postcode=serializer.data['postcode'],
                number=serializer.data['number'])
        except PostcodeLookupException:
            return Response(
                {
                    'error': 'No valid response received from backend'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(result.json())

    def get_serializer(self, **kwargs):
        return self.serializer_class(
            backend=self.backend, **kwargs)
