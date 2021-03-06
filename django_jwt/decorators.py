import functools

from jwt import decode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse

from .exceptions import (
    InvalidHeaderError,
    NoAuthorizationError,
)


def _load_user(identity):
    user_model = get_user_model()
    user = user_model.objects.filter(**identity).first()
    return user


def _decode_jwt_from_request(request):
    headers = request.META
    header_name = 'HTTP_AUTHORIZATION'
    header_type = 'Bearer'

    # Verify we have the auth header
    jwt_header = headers.get(header_name, None)
    if not jwt_header:
        raise NoAuthorizationError("Missing {} Header".format(header_name))

    # Make sure the header is in a valid format that we are expecting, ie
    # <HeaderName>: <HeaderType(optional)> <JWT>
    parts = jwt_header.split()
    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise InvalidHeaderError(msg)
        encoded_token = parts[0]
    else:
        if parts[0] != header_type or len(parts) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(header_name, header_type)
            raise InvalidHeaderError(msg)
        encoded_token = parts[1]

    decoded_token = decode(encoded_token, settings.SECRET_KEY, algorithms=['HS256'])
    if not decoded_token:
        raise NoAuthorizationError()
    return decoded_token


def jwt_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from django.conf import settings
        try:
            jwt_data = _decode_jwt_from_request(request)
        except (NoAuthorizationError, InvalidHeaderError) as e:
            return JsonResponse({settings.JWT['ERROR_MESSAGE_KEY']: str(e)}, status=401)
        identity_field = settings.JWT['IDENTITY_FIELD']
        identity = jwt_data[identity_field]
        user = _load_user({identity_field: identity})
        if not user:
            return JsonResponse({settings.JWT['ERROR_MESSAGE_KEY']: 'Invalid JWT'}, status=401)
        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper
