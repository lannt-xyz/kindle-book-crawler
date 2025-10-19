import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
        
class SmtpSender:
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
    
    @classmethod
    def init(cls):
        from config import settings
        return cls(
            smtp_server=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD
        )

    def send_email(self, from_addr, to_addrs, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs)

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(from_addr, to_addrs, msg.as_string())
    
    def send_email_with_attachment(self, from_addr, to_addrs, subject, body, attachment_path):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs)

        msg.attach(MIMEText(body, 'plain'))

        if not os.path.isfile(attachment_path):
            raise FileNotFoundError(f"Attachment not found: {attachment_path}")

        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(from_addr, to_addrs, msg.as_string())

