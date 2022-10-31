import datetime
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_api.models import Chats
from chat_message_api.models import Messages
from chat_user.models import User


@require_http_methods(['POST', ])
def create_message(request):
    body = json.loads(request.body)

    chat_id = body.get("chatId")
    author_id = body.get("authorId")
    content = body.get("content")

    user = get_object_or_404(User, id=author_id)
    chat = get_object_or_404(Chats, id=chat_id)

    if content and user.id in [item["id"] for item in chat.users.values()]:
        message = Messages(chat=chat, content=content, author=user)
        message.save()
        user.last_seen_at = datetime.datetime.now()
        user.save()
        chat.count_messages = len(chat.messages_in_chat.values())
        chat.save()

        return JsonResponse({"created": True}, status=201)

    return JsonResponse({"created": False}, status=400)


# почему тут еще понадобился GET? иначе не работало...
@require_http_methods(['DELETE', 'GET'])
def delete_message(request, pk):
    msg_obj = get_object_or_404(Messages, id=pk)
    msg_chat = msg_obj.chat_id
    chat = get_object_or_404(Chats, id=msg_chat)
    message_id = msg_obj.id

    if message_id:
        Messages(id=message_id).delete()
        chat.count_messages -= 1
        chat.save()

        return JsonResponse({"deleted": True, "idDeletedMessage": message_id}, status=200)

    return JsonResponse({"deleted": False}, status=400)


@require_http_methods(['PUT'])
def edit_message_content(request):
    body = json.loads(request.body)
    message_id = body.get("messageId")
    new_content = body.get("newContent")

    if message_id and new_content:
        message_obj = get_object_or_404(Messages, id=message_id)
        message_obj.content = new_content
        message_obj.save()

        return JsonResponse({"edited": True, "newContent": new_content}, status=200)

    return JsonResponse({"edited": False}, status=400)


@require_http_methods(['GET', ])
def get_message(request, pk):
    msg_model = get_object_or_404(Messages, id=pk)
    message = list(Messages.objects.filter(id=msg_model.id).values())

    for key, value in message[0].items():
        if isinstance(value, datetime.datetime):
            message[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")

    return JsonResponse({"msgInfo": message}, status=200)


@require_http_methods(['GET', ])
def get_messages_filter_user_chat(request):
    messages_chat_cur_user = []
    user_pk = int(request.GET.get("userId"))
    chat_pk = request.GET.get("chatId")
    messages_chat_sum = list(get_object_or_404(Chats, id=chat_pk).messages_in_chat.values())
    for elem in messages_chat_sum:
        if elem["author_id"] == user_pk:
            for key, value in elem.items():
                if isinstance(value, datetime.datetime):
                    elem[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
            messages_chat_cur_user.append(elem)

    return JsonResponse({"messages": messages_chat_cur_user}, status=200)


@require_http_methods(['GET', ])
def get_messages_filter_chat(request):
    messages_cur_chat = []
    chat_pk = request.GET.get("chatId")
    messages_chat_sum = list(get_object_or_404(Chats, id=chat_pk).messages_in_chat.values())
    for elem in messages_chat_sum:
        for key, value in elem.items():
            if isinstance(value, datetime.datetime):
                elem[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
                messages_cur_chat.append(elem)

    return JsonResponse({"messages": messages_cur_chat}, status=200)


@require_http_methods(['PUT', ])
def mark_message_as_viewed(request, pk):
    msg_model = get_object_or_404(Messages, id=pk)
    if not msg_model.viewed:
        msg_model.viewed = True
        msg_model.save()

        return JsonResponse({"viewed": True, "info": f"message with id {msg_model.id} mark as viewed"}, status=200)

    return JsonResponse({"viewed": False, "info": f"message with id {msg_model.id} is viewed already"}, status=400)
