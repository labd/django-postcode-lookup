from django_postcode_lookup.utils.version import get_version

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (2, 0, 0, "alpha", 0)

__version__ = get_version(VERSION)
