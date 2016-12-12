from django import template

from django_postcode_lookup import signing

register = template.Library()


@register.simple_tag
def postcode_lookup_key():
    return signing.create_api_key()
