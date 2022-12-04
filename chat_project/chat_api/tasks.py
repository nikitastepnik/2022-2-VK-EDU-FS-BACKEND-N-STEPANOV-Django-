from django.core.mail import send_mail

from chat_api.static.body_notification_new_member_in_chat import BODY_NOTIFICATION
from messenger.celery import app
from messenger.settings import EMAIL_HOST_USER, ADMINS


@app.task(time_limit=100)
def send_admin_email(chat_id, user_id):
    send_mail(subject='Notify about new member in chat',
              message=BODY_NOTIFICATION.format(user_id=user_id, chat_id=chat_id),
              from_email=EMAIL_HOST_USER,
              recipient_list=ADMINS)
