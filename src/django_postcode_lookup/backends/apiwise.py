from collections import namedtuple

import requests

from django_postcode_lookup.backends import base
from six.urllib.parse import urlencode


class _none(object):
    pass

_default = _none()

ENDPOINT = 'https://postcode-api.apiwise.nl/v2/addresses/'


AddressLookupResult = namedtuple(
    'AddressLookupResult', ['postcode', 'street', 'city'])


class ApiWise(base.Backend):
    _endpoint = 'https://postcode-api.apiwise.nl/v2/addresses/'

    def __init__(self, api_key, **kwargs):
        super(ApiWise, self).__init__(**kwargs)
        self._api_key = api_key

    def _get(self, postcode, number):
        postcode = postcode.replace(' ', '').upper()

        endpoint = ENDPOINT + '?' + urlencode({
            'postcode': postcode,
            'number': number
        })

        response = requests.get(endpoint, headers={
            'X-Api-Key': self.api_key
        })

        if response.status_code == 200:
            return _extract_results(response.json())


def _extract_results(data):
    if not data.get('_embedded') or not data['_embedded'].get('addresses'):
        return

    result = data['_embedded']['addresses'][0]

    postcode = result['postcode']
    street = result['street']
    city = result['city']['label']

    # format postcode to '1234 AA'
    if len(postcode) == 6:
        postcode = postcode[:4] + ' ' + postcode[4:]

    return base.AddressLookupResult(
        postcode=postcode,
        number=data['number'],
        city=city,
        street=street)
