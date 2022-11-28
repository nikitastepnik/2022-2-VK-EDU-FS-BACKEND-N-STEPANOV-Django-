from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from rest_framework.request import Request


def my_login_required(func):
    def wrapper(*args, **kwargs):
        request = None
        for elem in args:
            if isinstance(elem, WSGIRequest) or isinstance(elem, Request):
                request = elem

        if request:
            if request.COOKIES.get("sessionid") and request.COOKIES.get("csrftoken"):
                return func(*args, **kwargs)

        return login(request)

    return wrapper


@my_login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')
