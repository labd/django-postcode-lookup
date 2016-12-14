======================
django-postcode-lookup
======================

This Django app providers a pluggable postcode django restframework endpoint. It currently only works
for postcodes in The Netherlands.

Currently supports the following services:
 - ApiWise
 - Webservices.nl


Status
======
.. image:: https://travis-ci.org/LabD/django-postcode-lookup.svg?branch=master
    :target: https://travis-ci.org/LabD/django-postcode-lookup

.. image:: http://codecov.io/github/LabD/django-postcode-lookup/coverage.svg?branch=master 
    :target: http://codecov.io/github/LabD/django-postcode-lookup?branch=master
    
.. image:: https://img.shields.io/pypi/v/django-postcode-lookup.svg
    :target: https://pypi.python.org/pypi/django-postcode-lookup/

Installation
============

.. code-block:: shell

   pip install django_postcode_lookup
   
Usage
=====

Add the following to your urls.py:


.. code-block:: python

    url(r'^postcode-lookup/', include('django_postcode_lookup.urls')),


Add a setting with the required backend

.. code-block:: python

    POSTCODE_LOOKUP = {
        'default': {
            'backend': 'django_postcode_lookup.backends.Webservices',
            'OPTIONS': {
                'username': 'someuser',
                'password': 'somepassword',
            }
        }
    }


To offer some form of protection to the api endpoint for usage by others a 
valid csrf token is required.
