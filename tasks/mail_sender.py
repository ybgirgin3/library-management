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
    """
    A class to handle email notifications for overdue books and weekly reports.

    Attributes:
        CREDENTIALS (dict): Credentials for the email sender.
        OVERDUE_SUBJECT (str): Subject for the overdue email notifications.
        REPORT_SUBJECT (str): Subject for the weekly report email notifications.

    Methods:
        __init__: Initializes the Mail instance.
        overdue: Sends email notifications for overdue books.
        weekly_report: Sends weekly report email notifications.
        send: Sends an email to the specified recipient.
        create_html_body: Creates the HTML body for the email.

    """

    # CREDENTIALS = json.loads(open('.credentials.json'))
    CREDENTIALS = {
        'EMAIL': 'library_management@outlook.com',
        'PASSWORD': 'lm_system_9876'
    }
    OVERDUE_SUBJECT = 'You Have Books with Overdue\'d Date'
    REPORT_SUBJECT = 'Your Weekly Report is Here'

    def __init__(self,
                 receiver_mails: Union[str, List[str]],
                 data: Union[Dict, List[Dict]],
                 mail_type: str = None
                 ) -> None:
        self.smtp = smtplib.SMTP('smtp-mail.outlook.com', port=587)
        self.mail_type = 'overdue' if mail_type is None else 'report'
        self.receiver_mails = [receiver_mails] if isinstance(receiver_mails, str) else receiver_mails
        self.data = [data] if isinstance(data, str) else data
        self.email = self.create_html_body(DataFrame(self.data))

        # self.smtp.starttls()
        # self.smtp.login(self.CREDENTIALS['EMAIL'], self.CREDENTIALS['PASSWORD'])

    def overdue(self):
        """
        Sends email notifications for overdue books.
        """
        try:
            for rec in self.receiver_mails:
                self.email['From'] = self.CREDENTIALS['EMAIL']
                self.email['To'] = rec
                self.email['Subject'] = self.OVERDUE_SUBJECT
                self.send(rec)
        except Exception as e:
            print('error in overdue send mail', e, rec)

    def weekly_report(self):
        """
        Sends weekly report email notifications.
        """
        try:
            for rec in self.receiver_mails:
                self.email['From'] = self.CREDENTIALS['EMAIL']
                self.email['To'] = rec
                self.email['Subject'] = self.REPORT_SUBJECT
                self.send(rec)
        except Exception as e:
            print('error in weekly report send mail', e, rec)

    def send(self, receiver):
        """
        Sends an email to the specified recipient.

        Args:
            receiver (str): Email address of the recipient.
        """

        try:
            self.smtp.starttls()
            self.smtp.login(self.CREDENTIALS['EMAIL'], self.CREDENTIALS['PASSWORD'])

            self.smtp.sendmail(self.CREDENTIALS['EMAIL'], receiver, self.email.as_string())
            time.sleep(2)
            self.smtp.quit()
        except Exception as e:
            print('error while sending mail', e, receiver)

    def create_html_body(self, data: DataFrame):
        """
         Creates the HTML body for the email.

         Args:
             data (DataFrame): Data to be included in the email.

         Returns:
             MIMEMultipart: HTML email body.
         """

        body = f"""
            <html>
              <body>
                <p>Hi!<br>
                {self.OVERDUE_SUBJECT if self.mail_type == 'overdue' else self.REPORT_SUBJECT}
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
