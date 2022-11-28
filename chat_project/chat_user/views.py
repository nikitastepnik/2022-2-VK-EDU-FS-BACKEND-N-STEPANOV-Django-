from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from chat_auth.views import my_login_required
from chat_user.models import User
from chat_user.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        user_model = get_object_or_404(User, id=pk)
        user = UserSerializer(user_model)

        return JsonResponse({"user_info": user.data}, status=200)
