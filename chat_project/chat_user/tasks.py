import os

from chat_user.utils import get_count_current_online_users, insert_info_into_log_file
from messenger.celery import app


@app.task
def insert_information_about_cur_online():
    current_online_users = get_count_current_online_users()
    insert_info_into_log_file(os.getenv("LOG_FILE", "log_current_online.txt"), "Current online is: " + current_online_users)
