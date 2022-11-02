from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "count_messages")
    ordering = ["id"]
