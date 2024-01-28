import json
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict
from typing import List
from typing import Union

from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()


class Mail:
    smtp = smtplib.SMTP('smtp-mail.outlook.com', port=587)
    # CREDENTIALS = json.loads(open('.credentials.json'))
    CREDENTIALS = {
      'EMAIL': 'library_management@outlook.com',
      'PASSWORD': 'lm_system_9876'
    }
    OVERDUE_SUBJECT = 'You Have Books with Overdue\'d Date'
    REPORT_SUBJECT = 'Your Weekly Report is Here'

    def __init__(self, receiver_mails: Union[str, List[str]], overdue_data: Union[Dict, List[Dict]], mail_type: str = 'overdue'):
        self.receiver_mails = [receiver_mails] if isinstance(receiver_mails, str) else receiver_mails
        self.overdue_data = [overdue_data] if isinstance(overdue_data, str) else overdue_data
        self.email = self.create_html_body(DataFrame(self.overdue_data), _type=mail_type)

    def send_overdue(self):
        # [{'id': 3, 'patron_id': 1, 'book_id': 2,
        #         'checkout_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807),
        #         'refund_date': datetime.datetime(2024, 1, 27, 18, 46, 28, 897807), 'is_active': True}]

        self.smtp.starttls()
        self.smtp.login(self.CREDENTIALS['EMAIL'], self.CREDENTIALS['PASSWORD'])

        # create dataframe from overdue_data dict
        # dict_data = DataFrame(self.overdue_data)

        # self.email = self.create_html_body(dict_data, _type='overdue')

        for rec in self.receiver_mails:
            self.email['From'] = self.CREDENTIALS['EMAIL']
            self.email['To'] = rec
            self.email['Subject'] = self.OVERDUE_SUBJECT

            self.smtp.sendmail(self.CREDENTIALS['EMAIL'], rec, self.email.as_string())
            time.sleep(2)

        self.smtp.quit()

    def create_html_body(self, data: DataFrame, _type: str):
        body = f"""
            <html>
              <body>
                <p>Hi!<br>
                {self.OVERDUE_SUBJECT if _type == 'overdue' else self.REPORT_SUBJECT}
                {data.to_html(na_rep="", index=False).replace("<th>", "<th style = 'background-color: gray; color: white; text-align: center'>").replace("<td>", "<td style = 'text-align: start; padding: 10px;'>")}
                <br>
               </p>
              </body>
              <footer>
                Find an issue? Let me know
                Contact me <a href="http://ybgirgin3.github.io">Yusuf Berkay Girgin Personal Website</a>
              </footer>
            </html>
            """

        return MIMEMultipart('alternative', None, [MIMEText(body, 'html')])
