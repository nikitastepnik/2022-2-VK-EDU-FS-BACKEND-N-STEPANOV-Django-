from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_user.models import User
from chat_user.serializers import UserSerializer


@require_http_methods(['GET', ])
def get_user_info(request, pk):
    user_model = get_object_or_404(User, id=pk)
    user = UserSerializer(user_model)

    return JsonResponse({"user_info": user.data}, status=200)
