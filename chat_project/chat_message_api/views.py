import datetime
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_api.models import Chats
from chat_message_api.models import Messages
from chat_user.models import User


@require_http_methods(['POST', ])
def post_create_message(request):
    body = json.loads(request.body)

    chat_id = body.get("chatId")
    author_id = body.get("authorId")
    content = body.get("content")

    user = get_object_or_404(User, id=author_id)
    chat = get_object_or_404(Chats, id=chat_id)

    if content and user.id in (chat.companion_first.id, chat.companion_second, id):
        message = Messages(chat=chat, content=content, author=user)
        message.save()

        return JsonResponse({"created": True}, status=201)

    return JsonResponse({"created": False}, status=400)


# почему тут еще понадобился GET? иначе не работало...
@require_http_methods(['DELETE', 'GET'])
def delete_message(request, pk):
    message_id = get_object_or_404(Messages, id=pk).id

    if message_id:
        Messages(id=message_id).delete()
        return JsonResponse({"deleted": True}, status=200)

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
def get_message_list_user_chat(request):
    messages_chat_cur_user = []
    user_pk = int(request.GET.get("userId"))
    chat_pk = request.GET.get("chatId")
    messages_chat_sum = list(get_object_or_404(Chats, id=chat_pk).messages_in_chat.values())
    for idx_elem, elem in enumerate(messages_chat_sum):
        if elem["author_id"] == user_pk:
            for key, value in elem.items():
                if isinstance(value, datetime.datetime):
                    elem[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
            messages_chat_cur_user.append(elem)

    return JsonResponse({"messages": messages_chat_cur_user}, status=200)
