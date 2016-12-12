from django.conf.urls import url, include

urlpatterns = [
    url(r'^postcode-lookup/', include('django_postcode_lookup.urls')),
]
