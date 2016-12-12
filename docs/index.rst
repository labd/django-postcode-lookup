======================
django-postcode-lookup
======================

Pluggable postcode lookup endpoint

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
