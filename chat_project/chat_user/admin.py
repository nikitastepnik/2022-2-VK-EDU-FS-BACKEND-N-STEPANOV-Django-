from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "premium_status", "last_seen_at")
    ordering = ["-last_seen_at"]
