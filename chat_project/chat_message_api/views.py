from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets

from chat_api.models import Chat
from chat_auth.views import my_login_required
from chat_message_api.models import Message
from chat_message_api.serializers import MessageSerializer
from chat_message_api.utils import publish_message_to_websocket, clear_html_tags
from chat_user.models import User


class MessageViewSet(viewsets.ViewSet):
    def create(self, request):
        chat_id = request.POST.get("chat_id")
        author_id = request.POST.get("author_id")
        content = clear_html_tags(request.POST.get("content"))

        user = get_object_or_404(User, id=author_id)
        chat = get_object_or_404(Chat, id=chat_id)
        if content and user.id in [item["id"] for item in chat.users.values()]:
            Message.objects.create(chat_id=chat_id, author_id=author_id, content=content)
            user.last_seen_at = timezone.now()
            user.save()
            chat.count_messages = len(chat.messages_in_chat.values())
            chat.save()
            publish_message_to_websocket(MessageSerializer(chat.messages_in_chat,
                                                           many=True).data, channel="chat.id " + chat_id)
            return JsonResponse({"created": True, **{k: request.POST.get(k) for k in request.POST}}, status=201)

        return JsonResponse({"created": False}, status=400)

    @my_login_required
    def destroy(self, request, pk):
        msg_obj = get_object_or_404(Message, id=pk)
        chat = get_object_or_404(Chat, id=msg_obj.chat_id)

        if (request.user.id in chat.users and len(chat.users) == 2) or request.user.id in chat.admin:
            Message(id=msg_obj.id).delete()
            chat.count_messages -= 1
            if chat.count_messages == 0:
                chat.delete()
            else:
                chat.save()

            return JsonResponse({"deleted": True, "id_deleted_message": msg_obj.id}, status=200)

        return JsonResponse({"deleted": False, "msg_error": "You can not do it! You are not admin of chat or author"},
                            status=400)

    @my_login_required
    def partial_update_content(self, request, pk):
        msg_obj = get_object_or_404(Message, id=pk)
        if request.user.username == msg_obj.author and pk and get_object_or_404(Message, id=pk):
            Message.objects.filter(id=pk).update(**request.data)
            return JsonResponse({"edited": True, **request.data}, status=200)

        return JsonResponse({"edited": False}, status=400)

    @my_login_required
    def retrieve_without_filters(self, request, pk):
        msg_model = get_object_or_404(Message, id=pk)
        message = MessageSerializer(msg_model)

        return JsonResponse({"msg_info": message.data}, status=200)

    @my_login_required
    def partial_update_status(self, request, pk):
        msg_model = get_object_or_404(Message, id=pk)
        if request.user.username == msg_model.author and not msg_model.viewed:
            msg_model.viewed = True
            msg_model.save()

            return JsonResponse({"viewed": True, "info": f"message with id {msg_model.id} mark as viewed"}, status=200)

        return JsonResponse({"viewed": False, "info": f"message with id {msg_model.id} is viewed already"}, status=400)

    @my_login_required
    def retrieve_filter_user_and_chat(self, request):
        user_id = request.GET.get("user_id")
        chat_id = request.GET.get("chat_id")
        messages_chat = MessageSerializer(
            get_object_or_404(Chat, id=chat_id).messages_in_chat.filter(author_id=user_id),
            many=True)

        return JsonResponse({"messages": messages_chat.data}, status=200)

    def retrieve_filter_chat(self, request):
        chat_id = request.GET.get("chat_id")
        messages_chat = MessageSerializer(get_object_or_404(Chat, id=chat_id).messages_in_chat,
                                          many=True)

        return JsonResponse({"messages": messages_chat.data}, status=200)
