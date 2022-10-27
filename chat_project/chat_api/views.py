import datetime
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_api.models import Chats
from chat_user.models import User


@require_http_methods(['POST', ])
def post_create_chat(request):
    body = json.loads(request.body)

    topic = body.get("topic")
    companion_first = body.get("companionFirst")
    companion_second = body.get("companionSecond")

    if companion_first != companion_second:
        companion_first_model_obj = get_object_or_404(User, username=companion_first)
        companion_second_model_obj = get_object_or_404(User, username=companion_second)
    else:
        return JsonResponse({"created": False, "info": "companionFirst must be not equal companionSecond"}, status=400)

    if topic and companion_first_model_obj and companion_second_model_obj:
        chat = Chats(topic=topic,
                     companion_first=companion_first_model_obj,
                     companion_second=companion_second_model_obj)
        chat.save()

        return JsonResponse({"created": True}, status=201)

    return JsonResponse({"created": False}, status=400)


@require_http_methods(['DELETE', 'GET'])
def delete_chat(request, pk):
    chat_id = get_object_or_404(Chats, id=pk).id

    if chat_id:
        Chats(id=chat_id).delete()
        return JsonResponse({"deleted": True}, status=200)

    return JsonResponse({"deleted": False}, status=400)


# @api_view() - спросить про это и почему не робит -
# request.data (AttributeError: 'WSGIRequest' object has no attribute 'data')
@require_http_methods(['GET', ])
def get_chat(request, pk):
    chat_model = get_object_or_404(Chats, id=pk)
    chat = list(Chats.objects.filter(id=chat_model.id).values())
    for key, value in chat[0].items():
        if isinstance(value, datetime.datetime):
            chat[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")

    return JsonResponse({"chatInfo": chat}, status=200)


@require_http_methods(['GET', ])
def get_chats(request):
    chats = Chats.objects.all()

    chats = [
        {'id': chat.id,
         'topic': chat.topic,
         'created_at': chat.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
         'companion_first': chat.companion_first.username + ' ' + chat.companion_first.email,
         'companion_second': chat.companion_second.username + ' ' + chat.companion_first.email,
         'count_messages': str(chat.count_messages)} for chat in chats
    ]

    return JsonResponse({"items": chats}, status=200)


@require_http_methods(['GET', ])
def get_user_chats(request, user_pk):
    chats_user_as_comp_first = get_object_or_404(User, id=user_pk).comp_second.values()
    chats_user_as_comp_sec = get_object_or_404(User, id=user_pk).comp_first.values()
    chats_summary = list(chats_user_as_comp_first) + list(chats_user_as_comp_sec)

    for key, value in chats_summary[0].items():
        if isinstance(value, datetime.datetime):
            chats_summary[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")

    return JsonResponse({"items": chats_summary}, status=200)


@require_http_methods(['PUT'])
def edit_chat_topic(request):
    body = json.loads(request.body)
    chat_id = body.get("chatId")
    new_topic = body.get("newTopic")

    if chat_id and new_topic:
        chat_obj = get_object_or_404(Chats, id=chat_id)
        chat_obj.topic = new_topic
        chat_obj.save()

        return JsonResponse({"edited": True, "newTopic": new_topic}, status=200)

    return JsonResponse({"edited": False}, status=400)
