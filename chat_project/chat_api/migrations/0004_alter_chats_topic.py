# Generated by Django 4.1.2 on 2022-10-31 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('chat_api', '0003_remove_chats_companion_first_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='topic',
            field=models.TextField(default='Тематика чата', verbose_name='Название'),
        ),
    ]
