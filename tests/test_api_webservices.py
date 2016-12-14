import requests_mock
from rest_framework.test import APIRequestFactory

from django_postcode_lookup import loading, views


def test_api_webservices_valid(settings):
    rf = APIRequestFactory()

    settings.POSTCODE_LOOKUP = {
        'default': {
            'backend': 'django_postcode_lookup.backends.Webservices',
            'OPTIONS': {
                'username': 'someuser',
                'password': 'somepassword',
            }
        }
    }

    params = {
        'postcode': '3531 WR',
        'number': '1',
    }
    request = rf.post('/', data=params, format='json')

    views.PostcodeLookupView.backend = loading.get_backend()  # re-init backend
    view = views.PostcodeLookupView.as_view()

    with requests_mock.Mocker() as m:
        response = """
        <response>
          <reeksid>216778</reeksid>
          <huisnr_van>1</huisnr_van>
          <huisnr_tm>159</huisnr_tm>
          <wijkcode>3531</wijkcode>
          <lettercombinatie>WR</lettercombinatie>
          <reeksindicatie>0</reeksindicatie>
          <straatid>70283</straatid>
          <straatnaam>Niasstraat</straatnaam>
          <straatnaam_nen>Niasstraat</straatnaam_nen>
          <straatnaam_ptt>NIASSTR</straatnaam_ptt>
          <straatnaam_extract>NIASSTR</straatnaam_extract>
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
        """.strip()
        m.get(
            'https://ws1.webservices.nl/rpc/get-simplexml/utf-8/' +
            'addressReeksPostcodeSearch/someuser/somepassword/3531WR1',
            text=response)

        response = view(request)
        assert response.status_code == 200, response.rendered_content
        assert response.data == {
            'street': 'Niasstraat',
            'number': '1',
            'postcode': '3531 WR',
            'city': 'UTRECHT',
        }
