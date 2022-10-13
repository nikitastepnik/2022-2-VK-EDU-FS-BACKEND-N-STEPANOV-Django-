import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .static_mocks import list_chats_obj, page_chat_obj


@require_http_methods(['GET', ])
def list_of_chats(request):
    return JsonResponse(list_chats_obj, status=200)


@require_http_methods(['GET', ])
def page_chat(request):
    return JsonResponse(page_chat_obj, status=200)


@require_http_methods(['POST', ])
def create_chat(request):
    body = json.loads(request.body)

    chat_type = body.get("chatType")
    companion = body.get("companion")

    if chat_type and companion:
        return JsonResponse({"created": "true"}, status=201)

    return JsonResponse({"created": "false"}, status=400)
