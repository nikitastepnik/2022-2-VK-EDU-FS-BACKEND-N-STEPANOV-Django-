from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_online", "email", "premium_status", "last_seen_at")
    ordering = ["id"]
