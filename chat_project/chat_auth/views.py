from django.contrib.auth.views import LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.utils import timezone
from rest_framework.request import Request

from chat_user.models import User
from messenger import settings


def my_login_required(func):
    def wrapper(*args, **kwargs):
        request = None
        for elem in args:
            if isinstance(elem, WSGIRequest) or isinstance(elem, Request):
                request = elem
        #
        # if request:
        #     if request.COOKIES.get("sessionid") and request.COOKIES.get("csrftoken"):
        #         return func(*args, **kwargs)
        #
        # return login(request)
        return func(*args, **kwargs)

    return wrapper


@my_login_required
def home(request):
    User.objects.filter(id=request.user.id).update(is_online=True, last_seen_at=timezone.now())

    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    User.objects.filter(id=request.user.id).update(is_online=False, last_seen_at=timezone.now())

    return LogoutView.as_view(next_page=settings.LOGIN_URL)(request)
