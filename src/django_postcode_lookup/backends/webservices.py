from xml.etree import ElementTree as ET

import requests

from django_postcode_lookup.backends import base


class Webservices(base.Backend):
    _hostnames = [
        'ws1.webservices.nl',
        'ws2.webservices.nl'
    ]
    _endpoint_pattern = (
        'https://%(hostname)s/rpc/get-simplexml/utf-8/addressReeksPostcodeSearch/'
        '%(username)s/%(password)s/%(query)s')

    def __init__(self, username, password, **kwargs):
        super(Webservices, self).__init__(**kwargs)
        self._username = username
        self._password = password

    def _get(self, postcode, number):

        query = (postcode + str(number)).replace(' ', '').upper()

        for hostname in self._hostnames:
            endpoint = self._endpoint_pattern % {
                'hostname': hostname,
                'username': self._username,
                'password': self._password,
                'query': query
            }
            session = requests.session()
            session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
            session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

            try:
                response = session.get(endpoint)
            except requests.ConnectionError:
                raise base.PostcodeLookupException()

            if response.status_code == 200:
                result = _parse_response(response.content)
                if result:
                    return base.PostcodeLookupResult(
                        postcode=postcode,
                        number=number,
                        **result)
            raise base.PostcodeLookupException()


def _parse_response(content):
    """Return the XML response.

    A valid response is::

        <?xml version="1.0" encoding="UTF-8"?>
        <response>
          <reeksid>217158</reeksid>
          <huisnr_van>10</huisnr_van>
          <huisnr_tm>46</huisnr_tm>
          <wijkcode>3533</wijkcode>
          <lettercombinatie>JN</lettercombinatie>
          <reeksindicatie>1</reeksindicatie>
          <straatid>70376</straatid>
          <straatnaam>Ravellaan</straatnaam>
          <straatnaam_nen>Ravellaan</straatnaam_nen>
          <straatnaam_ptt>RAVELLN</straatnaam_ptt>
          <straatnaam_extract>RAVEL</straatnaam_extract>
          <plaatsid>440</plaatsid>
          <plaatsnaam>UTRECHT</plaatsnaam>
          <plaatsnaam_ptt>UTRECHT</plaatsnaam_ptt>
          <plaatsnaam_extract>UTRE</plaatsnaam_extract>
          <gemeenteid>137</gemeenteid>
          <gemeentenaam>UTRECHT</gemeentenaam>
          <gemeentecode>344</gemeentecode>
          <cebucocode>191</cebucocode>
          <provinciecode>M</provinciecode>
          <provincienaam>Utrecht</provincienaam>
        </response>

    When an error occurs the following is returned::

        <?xml version="1.0" encoding="UTF-8"?>
        <response>
          <fault>
            <faultCode>-32500</faultCode>
            <faultString>
              postcode::address_get_by_postcode::unknown_address :
              Could not find Postcode address '3533JN1'
            </faultString>
          </fault>
        </response>

    """
    document = ET.fromstring(content)
    fault = document.find('fault')
    if fault is not None:
        return None

    return {
        'street': document.find('straatnaam').text,
        'city': document.find('plaatsnaam').text,
    }
