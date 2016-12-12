import attr
from django.core.cache import cache


@attr.s
class PostcodeLookupResult(object):
    postcode = attr.ib()
    number = attr.ib()
    street = attr.ib()
    city = attr.ib()

    def json(self):
        return attr.asdict(self)


class PostcodeLookupException(IOError):
    pass


class _none(object):
    pass


class Backend(object):

    def __init__(self, cache_timeout=3600, validate_api_key=True):
        self._cache_timeout = cache_timeout
        self.validate_api_key = validate_api_key

    def lookup(self, postcode, number):
        query = (postcode + str(number)).replace(' ', '').upper()
        cache_key = 'dpl::%s' % query

        result = cache.get(cache_key, default=_none)
        if result is _none:
            result = self._get(postcode, number)
            cache.set(cache_key, result, self._cache_timeout)
        return result

    def _get(self, postcode, number):
        raise NotImplementedError()
