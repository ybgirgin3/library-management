import datetime

from celery import chain

from models import PatronModel
from routers.checkout import find_all
from services.orm import ORM
from tasks.beat import app
from tasks.mail_sender import Mail

patron_orm = ORM(model='PatronModel')


# get overdue tasks periodically
@app.task(name='task.get_overdues', bind=True)
def get_overdues(self):
    overdues = find_all(overdue=1).data
    if len(overdues):
        overdues_as_dict = [o.to_dict() for o in overdues]
        return overdues_as_dict
        # app.send_task(name='task.reminder', args=[overdues_as_dict], queue='send_reminder_mail')


@app.task(name='task.reminder_mail', bind=True)
def reminder(self, overdues: list[dict]):
    [{'id': 3, 'patron_id': 1, 'book_id': 2,
            'checkout_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807),
            'refund_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807),
            'is_active': True}]

    # find receiver_mail from overdue
    patron_ids: list = [d.get('patron_id') for d in overdues]

    # perform mail send
    for _id in patron_ids:
        rec: PatronModel = patron_orm.find_one({'id': _id})
        m = Mail(receiver_mails=rec.email, overdue_data=overdues)
        m.send_overdue()



@app.task(name='task.reporter')
def reporter():
    result_chain = chain(get_overdues.s(), reminder.s())
    print(result_chain())
