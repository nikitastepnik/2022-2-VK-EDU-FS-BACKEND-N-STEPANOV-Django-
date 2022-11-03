from rest_framework import serializers

from chat_user.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    premium_status = serializers.BooleanField()
    last_seen_at = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "premium_status", "last_seen_at")
