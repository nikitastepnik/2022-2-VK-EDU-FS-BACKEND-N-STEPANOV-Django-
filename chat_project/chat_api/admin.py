from django.contrib import admin

from .models import Chats


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ("topic", "companion_first", "companion_second", "count_messages")
