import datetime

from celery import Celery

# ◇ Create Celery tasks to automate the following library operations:   Send email
# reminders to patrons for overdue books.
# Generate weekly reports of book checkout statistics

app = Celery('library', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'task.reporter': {
        'task': 'task.reporter',
        'schedule': datetime.timedelta(seconds=10)
    },
    # 'minutely_reminder': {
    #     'task': 'task.reminder',
    #     'schedule': crontab(minute='*/1')
    # },
}

app.conf.result_backend = 'redis://localhost:6379/1'
