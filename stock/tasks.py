from celery import app

from .utils import find_reminders


@app.shared_task
def find_reminders_task():
    find_reminders()
