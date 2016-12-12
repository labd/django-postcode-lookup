from django.conf import settings
from django.utils.module_loading import import_string


def get_backend(name='default'):
    config = settings.POSTCODE_LOOKUP[name]
    backend = import_string(config['backend'])
    options = config.get('OPTIONS', {})
    return backend(**options)
