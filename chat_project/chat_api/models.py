from django.db import models

from chat_user.models import User


# ./manage.py shell
# psql -U python_backend_course -d chat_db

class Chats(models.Model):
    topic = models.TextField("Название", default="Базовое название")
    description = models.TextField("Описание", default="")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    users = models.ManyToManyField(User, verbose_name="Пользователи чата",
                                   related_name="chat_users")
    # companion_second = models.ForeignKey(User, verbose_name="Собеседник 2", on_delete=models.SET_NULL, null=True,
    #                                      related_name="comp_second")
    count_messages = models.IntegerField("Суммарное число сообщений", default=0)

    def __str__(self):
        return f"id: {self.id} topic: {self.topic}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
