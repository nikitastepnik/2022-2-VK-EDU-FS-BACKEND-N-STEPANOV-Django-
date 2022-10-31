from django.contrib import admin

from .models import Chats


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "count_messages")
    ordering = ["id"]
