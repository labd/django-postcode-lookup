from typing import Any, Dict, Optional

import requests

from django_postcode_lookup.backends import base


class PostcodeApiNu(base.Backend):

    def __init__(self, api_key: str, base_url: str, **kwargs):
        super(PostcodeApiNu, self).__init__(**kwargs)
        self._base_url = base_url
        self._session = requests.Session()
        self._session.headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }

    def _get(self, postcode: str, number: str) -> Optional[base.PostcodeLookupResult]:
        postcode = postcode.replace(' ', '').upper()

        url = f"{self._base_url}/{postcode}/{number}"

        response = self._session.get(url)

        if response.status_code == 200:
            return _extract_results(response.json())


def _extract_results(result: Dict[str, Any]) -> base.PostcodeLookupResult:
    postcode = result["postcode"]
    number = result['number']
    street = result["street"]
    city = result['city']

    # format postcode to '1234 AA'
    if len(postcode) == 6:
        postcode = postcode[:4] + ' ' + postcode[4:]

    return base.PostcodeLookupResult(
        postcode=postcode,
        number=number,
        city=city,
        street=street)
