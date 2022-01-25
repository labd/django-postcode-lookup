from django.urls import path

from django_postcode_lookup import views

urlpatterns = [
    path('', views.PostcodeLookupView.as_view(), name='postcode_lookup'),
]
