from django.middleware import csrf
from pretend import stub
from freezegun import freeze_time
from rest_framework.test import APIRequestFactory

from django_postcode_lookup import views
from django_postcode_lookup.backends.base import (
    PostcodeLookupException, PostcodeLookupResult)


def test_valid_api_key():
    rf = APIRequestFactory(enforce_csrf_checks=True)
    params = {
        'postcode': '3531 WR',
        'number': '1',
    }
    request = rf.post('/', data=params, format='json')
    csrf.rotate_token(request)
    request.COOKIES['csrftoken'] = request.META['CSRF_COOKIE']
    request.META['HTTP_X_CSRFTOKEN'] = request.META['CSRF_COOKIE']

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


def test_missing_csrf_key():
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


def test_handle_backend_exception():
    rf = APIRequestFactory(enforce_csrf_checks=True)
    params = {
        'postcode': '3531 WR',
        'number': '1',
    }
    request = rf.post('/', data=params, format='json')
    csrf.rotate_token(request)
    request.COOKIES['csrftoken'] = request.META['CSRF_COOKIE']
    request.META['HTTP_X_CSRFTOKEN'] = request.META['CSRF_COOKIE']

    def throw_error(postcode, number):
        raise PostcodeLookupException()

    views.PostcodeLookupView.backend = stub(lookup=throw_error)

    view = views.PostcodeLookupView.as_view()

    response = view(request)
    assert response.status_code == 400, response.rendered_content
    assert response.data == {
        'error': 'No valid response received from backend'
    }
