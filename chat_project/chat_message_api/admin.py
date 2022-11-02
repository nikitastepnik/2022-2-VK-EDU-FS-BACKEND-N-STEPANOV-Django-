from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "dispatch_date", "chat", "viewed")
    ordering = ["-dispatch_date"]
