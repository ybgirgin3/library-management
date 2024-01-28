import datetime
import os

import redis
from celery import Celery

# main_redis = redis.Redis(host='0.0.0.0', port=6379, db=0)
# backend_redis = redis.Redis(host='0.0.0.0', port=6379, db=1)
# app = Celery('library', broker=main_redis)

broker = 'redis://redis:6379/0'
backend_broker = 'redis://redis:6379/1'

if os.environ.get('DEBUG') == 1:
    broker = 'redis://localhost:6379/0'
    backend_broker = 'redis://localhost:6379/1'

app = Celery('library', broker=broker)


app.conf.result_backend = backend_broker
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
