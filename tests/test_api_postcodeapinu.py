import requests_mock
from rest_framework.test import APIRequestFactory

from django_postcode_lookup import loading, views


def test_api_postcodeapinu_valid(settings):
    rf = APIRequestFactory()

    settings.POSTCODE_LOOKUP = {
        'default': {
            'backend': 'django_postcode_lookup.backends.PostcodeApiNu',
            'OPTIONS': {
                'api_key': '1234abcd',
                'base_url': 'https://sandbox.postcodeapi.nu/v3/lookup',
            }
        }
    }

    params = {
        'postcode': '6545CA',
        'number': '29',
    }
    request = rf.post('/', data=params, format='json')

    views.PostcodeLookupView.backend = loading.get_backend()  # re-init backend
    view = views.PostcodeLookupView.as_view()

    with requests_mock.Mocker() as m:
        json_response = {
            "postcode": "6545CA",
            "number": 29,
            "street": "Binderskampweg",
            "city": "Nijmegen",
            "municipality": "Nijmegen",
            "province": "Gelderland",
            "location": {
                "type": "Point",
                "coordinates": [
                    5.858910083770752,
                    51.84376540294041
                ]
            }
        }
        m.get(
            "https://sandbox.postcodeapi.nu/v3/lookup/6545CA/29",
            json=json_response)

        response = view(request)
        assert response.status_code == 200, response.rendered_content
        assert response.data == {
            'street': 'Binderskampweg',
            'number': 29,
            'postcode': '6545 CA',
            'city': 'Nijmegen',
        }
