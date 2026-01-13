import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "milich.yulia@gmail.com"
APP_PASSWORD = "hpjf pepc icbc unxw"  # NOT your Gmail password
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

def create_server():
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    return server

def send_phishing_email(name, email, company):
    # Load HTML template
    with open(ATTACK_EMAIL_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Connect to Gmail
    server = create_server()

    # Personalize HTML
    personalized_html = html_template.replace("{{name}}", name)
    personalized_html = personalized_html.replace("{{company}}", company)

    # Build email
    msg = create_msg(personalized_html, email, ATTACK_SUBJECT+company)

    # Send
    server.sendmail(SENDER_EMAIL, email, msg.as_string())

    print(f"Sent attack to {name} <{email}>")
    server.quit()

def send_phishing_info_email(name, email, times_entered, pass_strength):
    # Load HTML template
    with open(INFO_EMAIL_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Connect to Gmail
    server = create_server()

    # Personalize HTML
    personalized_html = html_template.replace("{{name}}", name)
    personalized_html = personalized_html.replace("{{times_entered}}", times_entered)
    personalized_html = personalized_html.replace("{{pass_strength}}", pass_strength)

    # Build email
    msg = create_msg(personalized_html, email, INFO_SUBJECT)

    # Send
    server.sendmail(SENDER_EMAIL, email, msg.as_string())

    print(f"Sent to {name} <{email}>")
    server.quit()


send_phishing_email("Yulia Milich", "milich.yulia@gmail.com", "BGU")
send_phishing_info_email("Yulia Milich", "milich.yulia@gmail.com", "3", "0.5")