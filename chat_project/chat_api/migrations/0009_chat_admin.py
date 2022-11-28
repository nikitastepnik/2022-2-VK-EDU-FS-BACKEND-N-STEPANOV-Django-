# Generated by Django 4.1.2 on 2022-11-28 22:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_api', '0008_alter_chat_description_alter_chat_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_admin',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]