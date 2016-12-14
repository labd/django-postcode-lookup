from django.middleware.csrf import get_token as get_csrf_token
from freezegun import freeze_time
from pretend import stub
from rest_framework.test import APIRequestFactory

from django_postcode_lookup import views
from django_postcode_lookup.backends.base import PostcodeLookupResult


def test_valid_api_key(settings):
    rf = APIRequestFactory(enforce_csrf_checks=True)
    params = {
        'postcode': '3531 WR',
        'number': '1',
    }
    request = rf.post('/', data=params, format='json')
    csrf_token = get_csrf_token(request)
    request.COOKIES[settings.CSRF_COOKIE_NAME] = csrf_token
    request.META[settings.CSRF_HEADER_NAME] = csrf_token

    views.PostcodeLookupView.backend = stub(
        lookup=lambda postcode, number: PostcodeLookupResult(
            postcode='3531 WR',
            number='1',
            city='UTRECHT',
            street='Niasstraat'))

    view = views.PostcodeLookupView.as_view()

    response = view(request)
    assert response.status_code == 200, response.rendered_content
    assert response.data == {
        'street': 'Niasstraat',
        'number': '1',
        'postcode': '3531 WR',
        'city': 'UTRECHT',
    }


def test_missing_csrf_key(settings):
    rf = APIRequestFactory(enforce_csrf_checks=True)

    with freeze_time('2016-01-01 12:00'):
        params = {
            'postcode': '3531 WR',
            'number': '1',
        }

    request = rf.post('/', data=params, format='json')

    views.PostcodeLookupView.backend = stub(
        lookup=lambda postcode, number: PostcodeLookupResult(
            postcode='3531 WR',
            number='1',
            city='UTRECHT',
            street='Niasstraat'),
        validate_api_key=True)

    view = views.PostcodeLookupView.as_view()

    response = view(request)
    assert response.status_code == 403
    assert response.data == {
        'detail': 'CSRF Failed: CSRF cookie not set.'
    }
