from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.TextField("Номер телефона", blank=True)
    premium_status = models.BooleanField("Премиум статус", default=False)
    is_online = models.BooleanField("Online", default=False)
    last_seen_at = models.DateTimeField("Дата последнего посещения ресурса", auto_now=True)

    def __str__(self):
        return self.username + " " + self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
