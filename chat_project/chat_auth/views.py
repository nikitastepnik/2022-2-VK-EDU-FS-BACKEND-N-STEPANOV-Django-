from django.contrib.auth.views import LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import RedirectView
from rest_framework.decorators import api_view
from rest_framework.request import Request

from chat_user.models import User
from messenger import settings


def my_login_required(func):
    def wrapper(*args, **kwargs):
        request = None
        for elem in args:
            if isinstance(elem, WSGIRequest) or isinstance(elem, Request):
                request = elem

        if request:
            if User.objects.filter(csrf_token=request.request.COOKIES.get("csrftoken")).values()[0]["is_user_logged_in"]:
                return func(*args, **kwargs)

        return login(request)

    return wrapper


@my_login_required
def home(request):
    print(1234)
    User.objects.filter(id=request.user.id).update(is_online=True, last_seen_at=timezone.now())

    return render(request, 'home.html')


def login(request):
    return RedirectView.as_view(
        url=f'http://127.0.0.1:3000/2022-2-VK-EDU-FS-FRONTEND-N-STEPANOV#/')(request)


@my_login_required
def logout(request):
    User.objects.filter(id=request.user.id).update(is_online=False, is_user_logged_in=False, csrf_token="",
                                                   last_seen_at=timezone.now())

    return LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL)(request)


@api_view(['GET'])
def user_auth_success(request):
    User.objects.filter(id=request.user.id).update(is_online=True, is_user_logged_in=True, last_seen_at=timezone.now(),
                                                   csrf_token=request.COOKIES['csrftoken'])
    return RedirectView.as_view(
        url=f'http://127.0.0.1:3000/2022-2-VK-EDU-FS-FRONTEND-N-STEPANOV#/')(request)


@api_view(['GET'])
def user_auth(request):
    if not request.headers["X-XSRF-TOKEN"]:
        return HttpResponse(status=404)
    is_user_logged_in = User.objects.filter(csrf_token=request.headers["X-XSRF-TOKEN"]).values()[0]["is_user_logged_in"]
    user_id = User.objects.filter(csrf_token=request.headers["X-XSRF-TOKEN"]).values()[0]["id"]

    return JsonResponse({'is_user_logged_in': is_user_logged_in, 'user_id': user_id})
