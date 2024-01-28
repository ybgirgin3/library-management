import datetime

from celery import Celery

# ◇ Create Celery tasks to automate the following library operations:   Send email
# reminders to patrons for overdue books.
# Generate weekly reports of book checkout statistics

app = Celery('library', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'task.overdue_process': {
        'task': 'task.overdue_process',
        'schedule': datetime.timedelta(seconds=50)
    },
    'task.weekly_report': {
        'task': 'task.weekly_report',
        'schedule': datetime.timedelta(seconds=20)
    },
}

app.conf.result_backend = 'redis://localhost:6379/1'
