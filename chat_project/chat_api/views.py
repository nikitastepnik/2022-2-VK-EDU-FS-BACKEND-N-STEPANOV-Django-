from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from chat_api.models import Chat
from chat_api.serializers import ChatSerializer
from chat_api.tasks import send_admin_email
from chat_auth.views import my_login_required
from chat_message_api.serializers import MessageSerializer
from chat_user.models import User


class ChatViewSet(viewsets.ViewSet):
    def partial_update_add_user_to_chat(self, request):
        user_id = int(request.POST.get("user_id"))
        chat_id = request.POST.get("chat_id")
        user_obj = get_object_or_404(User, id=user_id)
        chat_obj = get_object_or_404(Chat, id=chat_id)

        if user_id not in [user["id"] for user in chat_obj.users.values()]:
            chat_obj.users.add(user_obj.id)
            send_admin_email(chat_id, user_id)
            return JsonResponse({"added": True, "info": f"user with {user_id} was added to chat with id {chat_id}"},
                                status=200)

        return JsonResponse({"added": False, "info": f"user with {user_id} "
                                                     f"has already been added to chat with id {chat_id}"}, status=400)

    @my_login_required
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

    @my_login_required
    def destroy(self, request, pk):
        chat = get_object_or_404(Chat, id=pk)
        if request.user.id in chat.admin:
            chat.delete()

            return JsonResponse({"deleted": True, "id_deleted_chat": pk}, status=200)

        return JsonResponse({"deleted": False, "msg_error": "You are not admin of this chat, you cannot destroy it!"},
                            status=400)

    @my_login_required
    def delete_member_from_chat(self, request):
        user_id = request.GET.get("user_id")
        chat_id = request.GET.get("chat_id")
        user_obj = get_object_or_404(User, id=user_id)
        chat_obj = get_object_or_404(Chat, id=chat_id)
        if request.user.id in chat_obj.admin and user_id in [item["id"] for item in chat_obj.users.values()]:
            chat_obj.users.remove(user_obj.id)

            return JsonResponse({"deleted": True, "info": f"user with {user_id} "
                                                          f"was deleted from chat with id {chat_id}"}, status=200)

        return JsonResponse({"deleted": False}, status=400)

    def retrieve(self, request, pk):
        chat_model = get_object_or_404(Chat, id=pk)
        chat = ChatSerializer(chat_model)

        return JsonResponse({"chat_info": chat.data}, status=200)

    def list_all_chats(self, request):
        chats = ChatSerializer(Chat.objects.all(), many=True)
        chats_data = list(chats.data)

        for idx, elem in enumerate(Chat.objects.all()):
            messages_in_chat = MessageSerializer(elem.messages_in_chat,
                                                 many=True)
            chats_data[idx]["last_message"] = messages_in_chat.data[len(messages_in_chat.data) - 1]

        chats_data.sort(key=lambda x: x["last_message"]["dispatch_date"], reverse=True)

        return JsonResponse({"items": chats_data}, status=200)

    @my_login_required
    def list_user_chats(self, request, user_pk):
        chats_user = get_object_or_404(User, id=user_pk).chat_users

        if not chats_user:
            return JsonResponse({"items": []}, status=200)

        chats_user = ChatSerializer(chats_user, many=True)

        return JsonResponse({"items": chats_user.data}, status=200)

    @my_login_required
    def update(self, request, pk):
        chat = get_object_or_404(Chat, id=pk)
        if request.user.id in chat.admin:
            Chat.objects.filter(id=pk).update(**request.POST)

            return JsonResponse({"edited": True, **request.POST}, status=200)

        return JsonResponse(
            {"edited": False, "msgError": "You can not update content of this chat! You are not admin of it!"},
            status=400)
