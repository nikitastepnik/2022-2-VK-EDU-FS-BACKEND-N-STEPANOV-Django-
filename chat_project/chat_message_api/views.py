import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view

from chat_api.models import Chat
from chat_message_api.models import Message
from chat_message_api.serializers import MessageSerializer
from chat_user.models import User


@require_http_methods(['POST', ])
def create_message(request):
    chat_id = request.POST.get("chat_id")
    author_id = request.POST.get("author_id")
    content = request.POST.get("content")

    user = get_object_or_404(User, id=author_id)
    chat = get_object_or_404(Chat, id=chat_id)

    if content and user.id in [item["id"] for item in chat.users.values()]:
        Message.objects.create(**{k: request.POST.get(k) for k in request.POST})
        user.last_seen_at = timezone.now()
        user.save()
        chat.count_messages = len(chat.messages_in_chat.values())
        chat.save()

        return JsonResponse({"created": True, **{k: request.POST.get(k) for k in request.POST}}, status=201)

    return JsonResponse({"created": False}, status=400)


@require_http_methods(['DELETE'])
def delete_message(request):
    msg_id = request.GET.get("message_id")
    msg_obj = get_object_or_404(Message, id=msg_id)
    chat = get_object_or_404(Chat, id=msg_obj.chat_id)

    Message(id=msg_obj.id).delete()
    chat.count_messages -= 1
    chat.save()

    return JsonResponse({"deleted": True, "id_deleted_message": msg_obj.id}, status=200)


@require_http_methods(['PUT'])
def edit_message_content(request):
    body = json.loads(request.body)
    message_id = body.pop("message_id")

    if message_id and get_object_or_404(Message, id=message_id):
        Message.objects.filter(id=message_id).update(**body)
        return JsonResponse({"edited": True, **body}, status=200)

    return JsonResponse({"edited": False}, status=400)


@require_http_methods(['GET', ])
def get_message(request, pk):
    msg_model = get_object_or_404(Message, id=pk)
    message = MessageSerializer(msg_model)

    return JsonResponse({"msg_info": message.data}, status=200)


@require_http_methods(['GET', ])
def get_messages_filter_user_chat(request):
    user_id = request.GET.get("user_id")
    chat_id = request.GET.get("chat_id")
    messages_chat = MessageSerializer(
        get_object_or_404(Chat, id=chat_id).messages_in_chat.filter(author_id=user_id),
        many=True)

    return JsonResponse({"messages": messages_chat.data}, status=200)


@require_http_methods(['GET', ])
def get_messages_filter_chat(request):
    chat_id = request.GET.get("chat_id")
    messages_chat = MessageSerializer(get_object_or_404(Chat, id=chat_id).messages_in_chat,
                                      many=True)

    return JsonResponse({"messages": messages_chat.data}, status=200)


@require_http_methods(['PUT', ])
def mark_message_as_viewed(request, pk):
    msg_model = get_object_or_404(Message, id=pk)

    if not msg_model.viewed and get_object_or_404(Message, id=pk):
        Message.objects.filter(id=pk).update(viewed=True)

        return JsonResponse({"viewed": True, "info": f"message with id {msg_model.id} mark as viewed"}, status=200)

    return JsonResponse({"viewed": False, "info": f"message with id {msg_model.id} is viewed already"}, status=400)
