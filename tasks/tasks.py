import datetime

from celery import chain

from routers.checkout import find_all
from tasks.beat import app


# get overdue tasks periodically
@app.task(name='task.get_overdues', bind=True)
def get_overdues(self):
    overdues = find_all(overdue=1).data
    if len(overdues):
        overdues_as_dict = [o.to_dict() for o in overdues]
        return overdues_as_dict
        # app.send_task(name='task.reminder', args=[overdues_as_dict], queue='send_reminder_mail')


@app.task(name='task.reminder', bind=True)
def reminder(self, overdues: list[dict]):
    return overdues


@app.task(name='task.reporter')
def reporter():
    result_chain = chain(get_overdues.s(), reminder.s())
    print(result_chain())
