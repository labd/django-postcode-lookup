from django.conf import settings
from django.utils.module_loading import import_string


def get_backend(name='default'):
    try:
        config = settings.POSTCODE_LOOKUP[name]
    except (KeyError, AttributeError):
        return

    backend = import_string(config['backend'])
    options = config.get('OPTIONS', {})
    return backend(**options)
