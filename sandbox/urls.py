from django.urls import include, path

urlpatterns = [
    path('postcode-lookup/', include('django_postcode_lookup.urls')),
]
