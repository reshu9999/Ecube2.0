import os
import smtplib

from flask import Flask
from subprocess import Popen, PIPE

from resources.responses import AetosBaseResponse
from resources.email_lib import EmailHandler
from resources.config_coordinator import config_fetcher

email_config = config_fetcher.get_email_config

email_app = dict()
email_app['SMTP_HOST'] = email_config['HOST']
email_app['SMTP_PORT'] = email_config['PORT']
email_app['USER'] = email_config['USER']
email_app['PASSWORD'] = email_config['PASSWORD']


class Emailer(EmailHandler):

    @classmethod
    def prepare_message(cls, send_to, subject, mail_body, cc=[], bcc=[]):
        message = EmailHandler._message(send_to, subject, mail_body, cc, bcc)
        return message
    
    @classmethod
    def add_attachments(cls, message, attachments):
        message = EmailHandler._attach_file(message, attachments)
        return message
    
    @classmethod
    def send_mail(cls, send_to, message):
        print('send_mail......')
        print(message)
        try:
            p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
            p.communicate(message.as_string())
            print('success...')
            return {'message': 'mail sent successfully', 'status': 'SUCCESS'}
        except Exception as e:
            print('failure...')
            print(e)
            return {'message': e.__str__(), 'status': 'FAILURE'}