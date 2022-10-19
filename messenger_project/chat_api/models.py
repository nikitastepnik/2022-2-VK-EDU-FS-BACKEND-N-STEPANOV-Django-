# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# psql -U python_backend_course -d chat_db
class User(AbstractUser):
    phone_number = models.TextField("Номер телефона", blank=True)
    premium_status = models.BooleanField("Премиум статус", default=False)
    last_seen_at = models.DateTimeField("Дата последнего посещения ресурса", auto_now_add=True)

    def __str__(self):
        return self.username + " " + self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Chats(models.Model):
    topic = models.TextField("Название", default="")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    companion_first = models.ForeignKey(User, verbose_name="Собеседник 1", on_delete=models.SET_NULL, null=True,
                                        related_name="comp_first")
    companion_second = models.ForeignKey(User, verbose_name="Собеседник 2", on_delete=models.SET_NULL, null=True,
                                         related_name="comp_sec")
    count_messages = models.IntegerField("Суммарное число сообщений", default=0)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


# ./manage.py shell