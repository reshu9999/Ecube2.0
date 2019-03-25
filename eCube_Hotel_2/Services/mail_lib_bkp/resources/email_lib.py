import threading
import pymysql
import os

from .custom_exceptions import GAIError

from smtplib import SMTP, SMTPAuthenticationError
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class EmailHandler(object):

    DEFAULT_ATTACHMENT_MIME_TYPE = 'application/octet-stream'

    DEFAULT_FROM_EMAIL = 'PricingTech@eclerx.com'

    @classmethod
    def _get_mail_object(cls, **config):
        try:
            mail_obj = SMTP(config['SMTP_HOST'], config['SMTP_PORT'])
        except GAIError as e:
            raise e

        mail_obj.starttls()

        try:
            mail_obj.login(config['USER'], config['PASSWORD'])
            return mail_obj
        except SMTPAuthenticationError as e:
            raise e

    @classmethod
    def _message(cls, to=None, subject='', body='', cc=None, bcc=None):

        msg = MIMEMultipart()
        msg['From'] = cls.DEFAULT_FROM_EMAIL
        msg['To'] = COMMASPACE.join(to) if isinstance(to,list) else to
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = COMMASPACE.join(cc) if isinstance(cc, list) else cc

        if bcc:
            msg['Bcc'] = COMMASPACE.join(bcc) if isinstance(bcc, list) else bcc

        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(body, 'html'))

        return msg

    @classmethod
    def _attach_file(cls, msg, files=[], mimetype=DEFAULT_ATTACHMENT_MIME_TYPE):
        for each in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(each,"rb").read() )
            part.add_header('Content-Disposition', 'attachment; filename="%s"'% os.path.basename(each))
            msg.attach(part)

        return msg