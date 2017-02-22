from django.core.exceptions import ImproperlyConfigured
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied
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

        self._enforce_csrf(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.backend.lookup(
            postcode=serializer.data['postcode'],
            number=serializer.data['number'])
            
        return Response(result.json())

    def get_serializer(self, **kwargs):
        return self.serializer_class(
            backend=self.backend, **kwargs)

    def _enforce_csrf(self, request):
        """Make sure that we have a valid CSRF token.

        Django restframework does validate this when using the
        SessionAuthentication but since that also checks if the user is
        authenticated we can't really use that

        """
        reason = CSRFCheck().process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise PermissionDenied('CSRF Failed: %s' % reason)
