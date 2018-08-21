import datetime

from jwt import encode

from django.conf import settings


def create_access_token(user):
    identity_field = settings.JWT['IDENTITY_FIELD']
    identity = getattr(user, identity_field)
    now = datetime.datetime.utcnow()
    payload = {identity_field: identity, 'iat': now}
    return encode(payload, settings.SECRET_KEY).decode()
