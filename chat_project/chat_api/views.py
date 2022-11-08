from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from chat_api.models import Chat
from chat_api.serializers import ChatSerializer
from chat_user.models import User


class ChatViewSet(viewsets.ViewSet):
    def partial_update_add_user_to_chat(self, request):
        user_id = int(request.POST.get("user_id"))
        chat_id = request.POST.get("chat_id")
        user_obj = get_object_or_404(User, id=user_id)
        chat_obj = get_object_or_404(Chat, id=chat_id)

        if user_id not in [user["id"] for user in chat_obj.users.values()]:
            chat_obj.users.add(user_obj.id)
            return JsonResponse({"added": True, "info": f"user with {user_id} was added to chat with id {chat_id}"},
                                status=200)

        return JsonResponse({"added": False, "info": f"user with {user_id} "
                                                     f"has already been added to chat with id {chat_id}"}, status=400)

    def create(self, request):
        users_id = request.data.pop("users_in_chat")

        if users_id:
            for user_id in users_id:
                get_object_or_404(User, id=user_id)
        else:
            return JsonResponse({"created": False, "msg_error": "'users_in_chat' must be set"}, status=400)

        chat = Chat.objects.create(**request.data)

        for user_id in users_id:
            chat.users.add(user_id)

        return JsonResponse({"created": True}, status=201)

    def destroy(self, request, pk):
        if pk and get_object_or_404(Chat, id=pk):
            Chat(id=pk).delete()
            return JsonResponse({"deleted": True, "id_deleted_chat": pk}, status=200)

        return JsonResponse({"deleted": False}, status=400)

    def delete_member_from_chat(self, request):
        user_id = request.GET.get("user_id")
        chat_id = request.GET.get("chat_id")
        user_obj = get_object_or_404(User, id=user_id)
        chat_obj = get_object_or_404(Chat, id=chat_id)

        if user_id in [item["id"] for item in chat_obj.users.values()]:
            chat_obj.users.remove(user_obj.id)
            return JsonResponse({"deleted": True, "info": f"user with {user_id} "
                                                          f"was deleted from chat with id {chat_id}"}, status=200)

        return JsonResponse({"deleted": False}, status=400)

    def retrieve(request, pk):
        chat_model = get_object_or_404(Chat, id=pk)
        chat = ChatSerializer(chat_model)

        return JsonResponse({"chat_info": chat.data}, status=200)

    def list_all_chats(self, request):
        chats = ChatSerializer(Chat.objects.all(), many=True)

        return JsonResponse({"items": chats.data}, status=200)

    def list_user_chats(self, request, user_pk):
        chats_user = get_object_or_404(User, id=user_pk).chat_users

        if not chats_user:
            return JsonResponse({"items": []}, status=200)

        chats_user = ChatSerializer(chats_user, many=True)

        return JsonResponse({"items": chats_user.data}, status=200)

    def update(self, request, pk):
        if get_object_or_404(Chat, id=pk):
            Chat.objects.filter(id=pk).update(**request.POST)

            return JsonResponse({"edited": True, **request.POST}, status=200)

        return JsonResponse({"edited": False}, status=400)
