import requests_mock
from rest_framework.test import APIRequestFactory

from django_postcode_lookup import loading, views


def test_api_apiwise_valid(settings):
    rf = APIRequestFactory()

    settings.POSTCODE_LOOKUP = {
        'default': {
            'backend': 'django_postcode_lookup.backends.ApiWise',
            'OPTIONS': {
                'api_key': '1234abcd',
            }
        }
    }

    params = {
        'postcode': '3625 KL',
        'number': '14',
    }
    request = rf.post('/', data=params, format='json')

    views.PostcodeLookupView.backend = loading.get_backend()  # re-init backend
    view = views.PostcodeLookupView.as_view()

    with requests_mock.Mocker() as m:
        response = {
            '_embedded': {
                'addresses': [
                    {
                        'postcode': '3625 KL',
                        'number': '14',
                        'street': 'Kanaalweg',
                        'city': {
                            'label': 'Utrecht'
                        }
                    }
                ]
            }
        }
        m.get(
            'https://postcode-api.apiwise.nl/v2/addresses/?postcode=3625KL&number=14',
            json=response)

        response = view(request)
        assert response.status_code == 200, response.rendered_content
        assert response.data == {
            'street': 'Kanaalweg',
            'number': '14',
            'postcode': '3625 KL',
            'city': 'Utrecht',
        }
