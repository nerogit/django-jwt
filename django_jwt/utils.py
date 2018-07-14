from jwt import encode

from django.conf import settings


def create_access_token(user):
    identity_field = settings.JWT['IDENTITY_FIELD']
    identity = getattr(user, identity_field)
    return encode(
        {identity_field: identity},
        settings.SECRET_KEY,
    ).decode()
