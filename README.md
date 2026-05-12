# django-postcode-lookup

This Django app provides a pluggable postcode Django REST Framework endpoint. It
currently only works for postcodes in The Netherlands.

Currently supports the following services:

    - ApiWise
    - Webservices.nl
    - postcodeapi.nu

## Status

[![Build Status](https://travis-ci.org/LabD/django-postcode-lookup.svg?branch=master)](https://travis-ci.org/LabD/django-postcode-lookup)
[![codecov](http://codecov.io/github/LabD/django-postcode-lookup/coverage.svg?branch=master)](http://codecov.io/github/LabD/django-postcode-lookup?branch=master)
[![PyPI](https://img.shields.io/pypi/v/django-postcode-lookup.svg)](https://pypi.python.org/pypi/django-postcode-lookup/)

## Installation

```shell
pip install django_postcode_lookup
```

## Usage

Add the following to your `urls.py`:

```python
path('postcode-lookup/', include('django_postcode_lookup.urls')),
```

Add a setting with the required backend

Webservices:

```python
POSTCODE_LOOKUP = {
    'default': {
        'backend': 'django_postcode_lookup.backends.Webservices',
        'OPTIONS': {
            'username': 'someuser',
            'password': 'somepassword',
        }
    }
}
```

ApiWise:

```python
POSTCODE_LOOKUP = {
    'default': {
        'backend': 'django_postcode_lookup.backends.ApiWise',
        'OPTIONS': {
            'api_key': 'somekey',
        }
    }
}
```

postcodeapi.nu:

```python
POSTCODE_LOOKUP = {
    'default': {
        'backend': 'django_postcode_lookup.backends.PostcodeApiNu',
        'OPTIONS': {
            'api_key': 'somekey',
            'base_url': 'https://somebaseurl.com',
        }
    }
}
```

To offer some form of protection to the api endpoint for usage by others a
valid csrf token is required.
