from email_connectors import Emailer


class MailHandler(object):

    @classmethod
    def mail_to(cls, mail_dict):
        print('mail dict...', mail_dict)
        message = Emailer.prepare_message(mail_dict['to'], mail_dict['subject'],
                                                mail_dict['body'], mail_dict.get('cc', []),
                                                mail_dict.get('bcc', []))

        if mail_dict['has_attachments'] is True:
            message = Emailer.add_attachments(message, mail_dict['attachments'])
        response = Emailer.send_mail(mail_dict['to'], message)
        return response
