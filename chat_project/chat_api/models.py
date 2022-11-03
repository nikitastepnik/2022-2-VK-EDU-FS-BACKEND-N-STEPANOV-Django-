from django.db import models

from chat_user.models import User


# ./manage.py shell
# psql -U python_backend_course -d chat_db

class Chat(models.Model):
    topic = models.TextField("Название", default="Базовое название")
    description = models.TextField("Описание", default="Базовое описание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    users = models.ManyToManyField(User, verbose_name="Пользователи чата",
                                   related_name="chat_users")
    count_messages = models.IntegerField("Суммарное число сообщений", default=0)

    def __str__(self):
        return f"id: {self.id} topic: {self.topic}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
