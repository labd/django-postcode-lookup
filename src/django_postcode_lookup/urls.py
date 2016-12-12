from django.conf.urls import url

from django_postcode_lookup import views

urlpatterns = [
    url(r'^$', views.PostcodeLookupView.as_view(), name='postcode_lookup'),
]
