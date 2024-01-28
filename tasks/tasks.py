import datetime
from typing import Dict
from typing import List

from celery import chain

from models import PatronModel
from routers.checkout import find_all as checkout_findall
from services.orm import ORM
from tasks.beat import app
from tasks.mail_sender import Mail

patron_orm = ORM(model='PatronModel')


# =========== checkouts begins ===============
@app.task(name='task.get_overdues', bind=True)
def get_overdues(self):
    overdues = checkout_findall(overdue=1).data
    if len(overdues):
        overdues_as_dict = [o.to_dict() for o in overdues]
        return overdues_as_dict
        # app.send_task(name='task.reminder', args=[overdues_as_dict], queue='send_reminder_mail')

@app.task(name='task.get_checkouts', bind=True)
def get_checkouts(self):
    checkouts_as_dict = [c.to_dict() for c in checkout_findall().data]
    if not len(checkouts_as_dict) or checkouts_as_dict is None:
        print('no checkouts found')

    return checkouts_as_dict

# =========== checkouts ends ===============


# =========== mails starts ===============
@app.task(name='task.reminder_mail', bind=True)
def reminder(self, overdues: List[Dict]):
    # [{'id': 3, 'patron_id': 1, 'book_id': 2,
    #         'checkout_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807),
    #         'refund_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807),
    #         'is_active': True}]

    # find receiver_mail from overdue
    patron_ids: List = [d.get('patron_id') for d in overdues]

    # perform mail send
    for _id in patron_ids:
        rec: PatronModel = patron_orm.find_one({'id': _id})
        m = Mail(receiver_mails=rec.email, data=overdues)
        m.overdue()
    return 'Overdue mail sending task is successfully finished'


@app.task(name='task.reporter', bind=True)
def reporter(self, checkouts: List[Dict]) -> str:
    patron_ids: List = list(set([d.get('patron_id') for d in checkouts]))

    # perform mail send
    for _id in patron_ids:
        try:
            rec: PatronModel = patron_orm.find_one({'id': _id, 'is_super': 1})
            m = Mail(receiver_mails=rec.email, data=checkouts, mail_type='report')
            m.weekly_report()
        except Exception as e:
            print('unable to continue to process due to: %s', e)

    return 'Weekly report sending task is successfully finished'

# =========== mails ends ===============


@app.task(name='task.process')
def process():
    result_chain = chain(get_overdues.s(), reminder.s())
    print(result_chain())
