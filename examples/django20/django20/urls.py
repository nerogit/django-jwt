from django.urls import path

from app.views import (
    ClassBasedView,
    func_view,
    sign_in,
)

urlpatterns = [
    path('cbv', ClassBasedView.as_view()),
    path('fbv', func_view),
    path('sign-in/', sign_in),
]
