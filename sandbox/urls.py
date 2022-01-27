from django.urls import path, include

urlpatterns = [
    path('postcode-lookup/', include('django_postcode_lookup.urls')),
]
