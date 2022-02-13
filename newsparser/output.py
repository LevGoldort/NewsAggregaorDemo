import smtplib
import ssl
import json

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(email: str, body: str):
    """
    Simple output to email
    :param email:
    :param body:
    :return: None
    """

    with open('config.json') as f:
        config_dict = json.load(f)

    from_email = config_dict['email']
    password = config_dict['password']

    port = 465
    context = ssl.create_default_context()
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(from_email, password)
        msg['Subject'] = 'Your news update'
        msg['From'] = from_email
        msg['To'] = email
        server.sendmail(msg['From'], msg['To'], msg.as_string())
