from rest_framework.test import APIRequestFactory

from django_postcode_lookup import signing, views
from django_postcode_lookup.backends.base import PostcodeLookupResult
from freezegun import freeze_time
from pretend import stub


def test_valid_api_key(settings):
    rf = APIRequestFactory()
    params = {
        'postcode': '3531 WR',
        'number': '1',
        'key': signing.create_api_key(),
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
    assert response.status_code == 200, response.rendered_content
    assert response.data == {
        'street': 'Niasstraat',
        'number': '1',
        'postcode': '3531 WR',
        'city': 'UTRECHT',
    }


def test_missing_api_key(settings, monkeypatch):
    rf = APIRequestFactory()

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
    assert response.status_code == 400
    assert response.data == {
        'key': ['This field is required.'],
    }


def test_old_api_key(settings, monkeypatch):
    rf = APIRequestFactory()

    with freeze_time('2016-01-01 12:00'):
        params = {
            'postcode': '3531 WR',
            'number': '1',
            'key': signing.create_api_key(),
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
    assert response.status_code == 400
    assert response.data == {
        'key': ['Invalid/expired key'],
    }


def test_disable_api_key(settings):
    rf = APIRequestFactory()
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
        validate_api_key=False)

    view = views.PostcodeLookupView.as_view()

    response = view(request)
    assert response.status_code == 200, response.rendered_content
    assert response.data == {
        'street': 'Niasstraat',
        'number': '1',
        'postcode': '3531 WR',
        'city': 'UTRECHT',
    }
