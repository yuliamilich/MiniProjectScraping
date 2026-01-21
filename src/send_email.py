import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import SENDER_EMAIL, APP_PASSWORD

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

ATTACK_SUBJECT = "Fwd: You received a voucher from "
INFO_SUBJECT = "You have fallen for a Phishing Scam"

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ATTACK_EMAIL_PATH = CURRENT_PATH+"/email/attack_email.html"
INFO_EMAIL_PATH = CURRENT_PATH+"/email/info_email.html"

def create_msg(html, email, subject):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))
    return msg

def _send(msg, to_email: str):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    except smtplib.SMTPRecipientsRefused as exc:
        raise RuntimeError(f"Recipient refused: {to_email}") from exc
    except smtplib.SMTPAuthenticationError as exc:
        raise RuntimeError("SMTP authentication failed") from exc
    except smtplib.SMTPException as exc:
        raise RuntimeError(f"SMTP error: {exc}") from exc

def send_phishing_email(name, email, company, fake_url):
    with open(ATTACK_EMAIL_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    personalized_html = html_template.replace("{{name}}", name)
    personalized_html = personalized_html.replace("{{company}}", company)
    personalized_html = personalized_html.replace("{{URL}}", fake_url)

    msg = create_msg(personalized_html, email, ATTACK_SUBJECT+company)

    _send(msg, email)
    print(f"Sent attack to {name} <{email}>")

def send_phishing_info_email(name, email, times_entered, pass_strength):
    with open(INFO_EMAIL_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    personalized_html = html_template.replace("{{name}}", name)
    personalized_html = personalized_html.replace("{{times_entered}}", str(times_entered))
    personalized_html = personalized_html.replace("{{pass_strength}}", str(pass_strength))

    msg = create_msg(personalized_html, email, INFO_SUBJECT)

    _send(msg, email)
    print(f"Sent to {name} <{email}>")
