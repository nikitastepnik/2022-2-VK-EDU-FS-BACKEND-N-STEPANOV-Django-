import datetime
import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat_api.models import Chat
from chat_api.serializers import ChatSerializer
from chat_user.models import User


@require_http_methods(['POST', ])
def add_user_to_chat(request):
    body = json.loads(request.body)
    user_id = body.get("userId")
    chat_id = body.get("chatId")
    user_obj = get_object_or_404(User, id=user_id)
    chat_obj = get_object_or_404(Chat, id=chat_id)

    if user_id not in [user["id"] for user in chat_obj.users.values()]:
        chat_obj.users.add(user_obj.id)
        return JsonResponse({"added": True, "info": f"user with {user_id} was added to chat with id {chat_id}"},
                            status=200)

    return JsonResponse({"added": False, "info": f"user with {user_id} "
                                                 f"has already been added to chat with id {chat_id}"}, status=400)


@require_http_methods(['POST', ])
def create_chat(request):
    body = json.loads(request.body)
    users_id = body.pop("usersInChat")

    if users_id:
        for user_id in users_id:
            get_object_or_404(User, id=user_id)
    else:
        return JsonResponse({"created": False, "msgError": "'usersInChat' must be set"}, status=400)

    chat = Chat.objects.create(**body)

    for user_id in users_id:
        chat.users.add(user_id)

    return JsonResponse({"created": True}, status=201)


@require_http_methods(['DELETE', 'GET'])
def delete_chat(request, pk):
    if pk and get_object_or_404(Chat, id=pk):
        Chat(id=pk).delete()
        return JsonResponse({"deleted": True, "idDeletedChat": pk}, status=200)

    return JsonResponse({"deleted": False}, status=400)


@require_http_methods(['DELETE', 'GET'])
def delete_member_from_chat(request):
    body = json.loads(request.body)
    user_id = body.get("userId")
    chat_id = body.get("chatId")
    user_obj = get_object_or_404(User, id=user_id)
    chat_obj = get_object_or_404(Chat, id=chat_id)

    if user_id in [item["id"] for item in chat_obj.users.values()]:
        chat_obj.users.remove(user_obj.id)
        return JsonResponse({"deleted": True, "info": f"user with {user_id} "
                                                      f"was deleted from chat with id {chat_id}"}, status=200)

    return JsonResponse({"deleted": False}, status=400)


@require_http_methods(['GET', ])
def get_chat(request, pk):
    chat_model = get_object_or_404(Chat, id=pk)
    chat = ChatSerializer(chat_model)

    return JsonResponse({"chatInfo": chat.data}, status=200)


@require_http_methods(['GET', ])
def get_chats(request):
    chats = ChatSerializer(Chat.objects.all(), many=True)

    return JsonResponse({"items": chats.data}, status=200)


@require_http_methods(['GET', ])
def get_user_chats(request, user_pk):
    chats_user = get_object_or_404(User, id=user_pk).chat_users

    if not chats_user:
        return JsonResponse({"items": []}, status=200)

    chats_user = ChatSerializer(chats_user, many=True)

    return JsonResponse({"items": chats_user.data}, status=200)


@require_http_methods(['PUT'])
def edit_chat_information(request):
    body = json.loads(request.body)
    chat_id = body.pop("chatId")
    if get_object_or_404(Chat, id=chat_id):
        Chat.objects.filter(id=chat_id).update(**body)

        return JsonResponse({"edited": True, **body}, status=200)

    return JsonResponse({"edited": False}, status=400)
