# django-postcode-lookup

This Django app provides a pluggable postcode Django REST Framework endpoint. It
currently only works for postcodes in The Netherlands.

Currently supports the following services:

    - ApiWise
    - Webservices.nl
    - postcodeapi.nu

## Status

[![PyPI](https://img.shields.io/pypi/v/django-postcode-lookup.svg)](https://pypi.python.org/pypi/django-postcode-lookup/)

## Installation

```shell
pip install django_postcode_lookup
```

Minimum supported Django version: 5.2 (Django 6 supported)

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

## Changelog and releases

This project uses [changie](https://changie.dev/) for changelog management.

Add a changelog fragment in pull requests with:

```shell
changie new
```

To prepare a release, run the `Prepare release PR` GitHub Actions workflow. It batches unreleased fragments, updates `CHANGELOG.md` and version files, then opens a release pull request. Merging that release PR publishes the package and creates the GitHub release from the changelog entry.
