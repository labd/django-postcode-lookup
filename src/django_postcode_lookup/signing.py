import uuid

from django.core.signing import TimestampSigner, SignatureExpired  # noqa


def create_api_key():
    value = uuid.uuid4().hex[:6]
    signer = TimestampSigner()
    return signer.sign(value)


def validate_api_key(key):
    signer = TimestampSigner()
    return signer.unsign(key, max_age=1800)
