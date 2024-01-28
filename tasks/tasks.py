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

overdue_mock = [{'id': 1,
                 'patron_id': 1,
                 'book_id': 1,
                 'checkout_date': datetime.datetime(2024, 1, 28, 14, 55, 0, 50152),
                 'refund_date': datetime.datetime(2024, 1, 28, 14, 55, 0, 51317),
                 'is_active': True}]

checkout_mock = [{'id': 1,
                  'patron_id': 1,
                  'book_id': 1,
                  'checkout_date': datetime.datetime(2024, 1, 28, 14, 55, 0, 50152),
                  'refund_date': datetime.datetime(2024, 1, 28, 14, 55, 0, 51317),
                  'is_active': True}]


# =========== checkouts begins ===============
@app.task(name='task.get_overdues', bind=True)
def get_overdues(self):
    """
    Retrieve overdue checkouts from the database.
    """

    overdues = checkout_findall(overdue=1).data
    if not overdues or not len(overdues):
        return None

    overdues_as_dict = [o.to_dict() for o in overdues]
    return overdues_as_dict


@app.task(name='task.get_checkouts', bind=True)
def get_checkouts(self):
    """
    Retrieve all checkouts from the database.
    """

    checkouts_as_dict = [c.to_dict() for c in checkout_findall().data]
    if not len(checkouts_as_dict) or checkouts_as_dict is None:
        print('no checkouts found')

    return checkouts_as_dict


# =========== checkouts ends ===============


# =========== mails starts ===============
@app.task(name='task.reminder_mail', bind=True)
def reminder(self, overdues: List[Dict]):
    """
    Send reminder emails to patrons with overdue checkouts.
    """

    # find receiver_mail from overdue
    patron_ids: List = [d.get('patron_id') for d in overdues]

    # perform mail send
    for _id in patron_ids:
        rec: PatronModel = patron_orm.find_one({'id': _id})
        if rec is None:
            print(f'Unable to find email from current rec: {rec}')
            continue
        m = Mail(receiver_mails=rec.email, data=overdues)
        m.overdue()
    return 'Overdue mail sending task is successfully finished'


@app.task(name='task.reporter', bind=True)
def reporter(self, checkouts: List[Dict]) -> str:
    """
    Send weekly report emails to super patrons.
    """

    patron_ids: List = list(set([d.get('patron_id') for d in checkouts]))

    # perform mail send
    for _id in patron_ids:
        try:
            rec: PatronModel = patron_orm.find_one({'id': _id, 'is_super': 1})
            if rec is None:
                print(f'Unable to find email from current rec: {rec}')
                continue
            m = Mail(receiver_mails=rec.email, data=checkouts, mail_type='report')
            m.weekly_report()
        except Exception as e:
            print('unable to continue to process due to: %s', e)

    return 'Weekly report sending task is successfully finished'


# =========== mails ends ===============


@app.task(name='task.overdue_process')
def overdue_process():
    """
    Chain for processing overdue checkouts.
    """
    result_chain = chain(get_overdues.s(), reminder.s())
    print(result_chain())


@app.task(name='task.weekly_report')
def weekly_report_process():
    """
    Chain for processing weekly reports.
    """

    result_chain = chain(get_checkouts.s(), reporter.s())
    print(result_chain())
