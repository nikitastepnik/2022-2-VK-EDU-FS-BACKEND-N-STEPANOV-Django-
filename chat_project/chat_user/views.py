import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_user.models import User


@require_http_methods(['GET', ])
def get_user_info(request, pk):
    user_model = get_object_or_404(User, id=pk)
    user = list(User.objects.filter(id=user_model.id).values())

    for key, value in user[0].items():
        if key == "password":
            user[0][key] = "*********"
        if isinstance(value, datetime.datetime):
            user[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")

    return JsonResponse({"msgInfo": user}, status=200)
