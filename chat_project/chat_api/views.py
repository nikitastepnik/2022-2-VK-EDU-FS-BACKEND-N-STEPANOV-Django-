import datetime
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_api.models import Chats
from chat_user.models import User


@require_http_methods(['POST', ])
def add_user_to_chat(request):
    body = json.loads(request.body)
    user_id = body.get("userId")
    chat_id = body.get("chatId")
    if user_id:
        user_obj = get_object_or_404(User, id=user_id)
        if chat_id:
            chat_obj = get_object_or_404(Chats, id=chat_id)
            if user_id not in [user["id"] for user in chat_obj.users.values()]:
                chat_obj.users.add(user_obj.id)
                return JsonResponse({"added": True, "info": f"user with {user_id} was added to chat with id {chat_id}"},
                                    status=200)

    return JsonResponse({"added": False, "info": f"user with {user_id} "
                                                 f"has already been added to chat with id {chat_id}"}, status=400)


@require_http_methods(['POST', ])
def create_chat(request):
    body = json.loads(request.body)

    topic = body.get("topic")
    description = body.get("description")
    users_id = body.get("usersInChat")
    if users_id:
        for user_id in users_id:
            get_object_or_404(User, id=user_id)
    else:
        return JsonResponse({"created": False, "msgError": "'usersInChat' must be set"}, status=400)

    if topic and description:
        chat = Chats(topic=topic, description=description)
    elif topic:
        chat = Chats(topic=topic)
    elif description:
        chat = Chats(description=description)
    else:
        chat = Chats()
    chat.save()

    for user_id in users_id:
        chat.users.add(user_id)

    return JsonResponse({"created": True}, status=201)


@require_http_methods(['DELETE', 'GET'])
def delete_chat(request, pk):
    chat_id = get_object_or_404(Chats, id=pk).id

    if chat_id:
        Chats(id=chat_id).delete()
        return JsonResponse({"deleted": True, "idDeletedChat": chat_id}, status=200)

    return JsonResponse({"deleted": False}, status=400)


@require_http_methods(['DELETE', 'GET'])
def delete_member_from_chat(request):
    body = json.loads(request.body)
    user_id = body.get("userId")
    chat_id = body.get("chatId")
    if user_id:
        user_obj = get_object_or_404(User, id=user_id)
        if chat_id:
            chat_obj = get_object_or_404(Chats, id=chat_id)
            if user_id in [item["id"] for item in chat_obj.users.values()]:
                chat_obj.users.remove(user_obj.id)
                return JsonResponse({"deleted": True, "info": f"user with {user_id} "
                                                              f"was deleted from chat with id {chat_id}"}, status=200)

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
         'usersIds': [user["id"] for user in chat.users.values()],  # как сделать отображение в 1 строку ?
         'count_messages': str(chat.count_messages)} for chat in chats
    ]

    return JsonResponse({"items": chats}, status=200)


@require_http_methods(['GET', ])
def get_user_chats(request, user_pk):
    chats_user = list(get_object_or_404(User, id=user_pk).chat_users.values())

    if not chats_user:
        return JsonResponse({"items": []}, status=200)

    for key, value in chats_user[0].items():
        if isinstance(value, datetime.datetime):
            chats_user[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")

    return JsonResponse({"items": chats_user}, status=200)


@require_http_methods(['PUT'])
def edit_chat_information(request):
    body = json.loads(request.body)
    chat_id = body.get("chatId")
    new_topic = body.get("newTopic")
    new_description = body.get("newDescription")

    if chat_id and (new_topic or new_description):
        chat_obj = get_object_or_404(Chats, id=chat_id)
        if new_description:
            chat_obj.description = new_description
        if new_topic:
            chat_obj.topic = new_topic
        chat_obj.save()

        if new_topic and new_description:
            return JsonResponse({"edited": True, "newTopic": new_topic, "newDescription": new_description},
                                status=200)
        elif new_topic:
            return JsonResponse({"edited": True, "newTopic": new_topic}, status=200)
        elif new_description:
            return JsonResponse({"edited": True, "newDescription": new_description}, status=200)

    return JsonResponse({"edited": False}, status=400)
