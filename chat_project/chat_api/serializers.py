from rest_framework import serializers

from chat_api.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(max_length=1)
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    count_messages = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('id', 'description', 'topic', 'created_at', 'users', 'count_messages')
