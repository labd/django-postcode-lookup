======================
django-postcode-lookup
======================

Pluggable postcode lookup endpoint

Status
======
.. image:: https://travis-ci.org/labd/django-postcode-lookup.svg?branch=master
    :target: https://travis-ci.org/labd/django-postcode-lookup

.. image:: http://codecov.io/github/labd/django-postcode-lookup/coverage.svg?branch=master 
    :target: http://codecov.io/github/labd/django-postcode-lookup?branch=master
    
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

    POSTCODE_LOOKUP_BACKEND = 'django_postcode_lookup.backend.webservices_nl'
