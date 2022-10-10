import json

from django.http import HttpResponseNotAllowed, JsonResponse

from .static_mocks import list_chats_obj, page_chat_obj


def list_of_chats(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET', ], status=405)

    return JsonResponse(list_chats_obj, status=200)


def page_chat(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET', ], status=405)

    return JsonResponse(page_chat_obj, status=200)


def create_chat(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST', ], status=405)

    body = json.loads(request.body)

    chat_type = body.get("chatType")
    companion = body.get("companion")

    if chat_type and companion:
        return JsonResponse({"created": "true"}, status=201)

    return JsonResponse({"created": "false"}, status=400)
