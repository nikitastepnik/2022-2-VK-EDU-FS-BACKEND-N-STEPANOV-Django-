from django.db import models

from chat_user.models import User


# ./manage.py shell
# psql -U python_backend_course -d chat_db

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
