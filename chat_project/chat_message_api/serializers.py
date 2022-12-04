from rest_framework import serializers

from chat_message_api.models import Message


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    dispatch_date = serializers.DateTimeField()
    author = serializers.CharField()
    chat = serializers.CharField()
    viewed = serializers.BooleanField()

    class Meta:
        model = Message
        fields = ('id', 'content', 'dispatch_date', 'author', 'chat', 'viewed')
