# Create your models here.
from django.db import models


class User(models.Model):
    login = models.TextField()
    password = models.TextField()
    email = models.TextField(blank=True)
    phone_number = models.TextField(blank=True)
    premium_status = models.BooleanField(default=False)
    registration_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now_add=True)


class ChatsList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.TextField(default="")
    companion_first = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comp_first")
    companion_second = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comp_set")
    # спросить про related_name
    count_messages = models.IntegerField(default=0)
