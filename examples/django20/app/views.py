from django_jwt import (
    create_access_token,
    jwt_required,
)

from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View


@jwt_required
def func_view(request):
    user = request.user
    results = {"username": user.username}
    return JsonResponse(results)


@method_decorator(jwt_required, name='dispatch')
class ClassBasedView(View):
    def get(self, request):
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
