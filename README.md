# Django JWT

Inspired by [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended)

## Installation

`pip install git+https://github.com/nerogit/django-jwt.git`

## Usage

```python
from django_jwt import (
    create_access_token,
    jwt_required,
)

from django.contrib.auth import authenticate
from django.http.response import JsonResponse


@jwt_required
def func_view(request):
    user = request.user
    results = {"username": user.username}
    return JsonResponse(results)



def sign_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        access_token = create_access_token(user)
    else:
        return JsonResponse({}, status=401)

    return JsonResponse({"accessToken": access_token})
```

