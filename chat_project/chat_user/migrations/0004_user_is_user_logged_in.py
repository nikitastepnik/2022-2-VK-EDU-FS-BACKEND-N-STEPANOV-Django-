# Generated by Django 4.1.2 on 2022-12-09 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_user', '0003_alter_user_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_user_logged_in',
            field=models.BooleanField(default=False, verbose_name='User Login Status'),
        ),
    ]
