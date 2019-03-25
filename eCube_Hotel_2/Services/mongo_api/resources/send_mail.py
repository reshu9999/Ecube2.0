from smtplib import SMTP
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# Default MIME type to use on attachments (if it is not explicitly given
# and cannot be guessed).
DEFAULT_ATTACHMENT_MIME_TYPE = 'application/octet-stream'


DEFAULT_FROM_EMAIL = 'eCube2_TechTeam@eclerx.com'

class EmailMessage(object):
    """A container for email information."""

    @classmethod
    def _get_connection(cls):
        mail_obj = SMTP('smtp1.eclerx.com', 25)
        mail_obj.starttls()
        username = ''
        password = ''
        mail_obj.login(username, password)
        return mail_obj

    @classmethod
    def _message(cls, subject='', body='', from_email=None, to=None, cc=None, bcc=None):

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email or DEFAULT_FROM_EMAIL
        msg['To'] = COMMASPACE.join(to) if isinstance(to,list) else to

        if cc:
            msg['Cc'] = COMMASPACE.join(cc) if isinstance(cc, list) else cc

        if bcc:
            msg['Bcc'] = COMMASPACE.join(bcc) if isinstance(bcc, list) else bcc

        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(body, 'html'))

        return msg

    @classmethod
    def _attach_file(cls, msg, path=None, files=None, mimetype=DEFAULT_ATTACHMENT_MIME_TYPE):
        if files is not None and isinstance(files, list):
            for path in files:
                part = MIMEBase('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
        return msg.attach(part)

    @classmethod
    def _send(cls, send_from, send_to, msg):
        """Send the email message."""
        resp = cls._get_connection().sendmail(send_from, send_to, msg.as_string())
        return resp

    @classmethod
    def send_mail(cls, subject='', body='', from_email=None, to=None, cc=None, bcc=None, files=None):
        import pdb; pdb.set_trace()
        msg = cls._message(subject, body, from_email, to, cc, bcc)
        # if files is not None:
            # msg = cls._attach_file(path = '', files)
        response = cls._send(from_email, to, msg)
        return response

if __name__ == "__main__":
    EmailMessage.send_mail(subject="Test", body="<body><h1>Test E-mail</h1></body>",
                        from_email="punit.kenia@eclerx.com",to="punit.kenia@eclerx.com",
                        cc="punit.kenia@eclerx.com", bcc="punit.kenia@eclerx.com")