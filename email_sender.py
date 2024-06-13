import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def send_email(rows, timestamp):
    logger.info("Entering send_email function")
    logger.info(f"Received {len(rows)} rows of data")

    with open('.credentials.yaml', 'r') as f:
        logger.info("Loading credentials from.credentials.yaml")
        credentials = yaml.safe_load(f)

    logger.info("Creating email message")
    msg = MIMEMultipart()
    msg['From'] = credentials['email_server']['username']
    msg['To'] = ', '.join(map(str, credentials['email']['to'])) if isinstance(credentials['email']['to'], list) else credentials['email']['to']
    msg['CC'] = ', '.join(map(str, credentials['email']['cc'])) if isinstance(credentials['email']['cc'], list) else credentials['email']['cc']
    msg['Subject'] = credentials['email']['email_subject']

    logger.info("Processing unique names")
    unique_names = set((row[0], row[1], row[2]) for row in rows)
    count = len(unique_names)
    logger.info(f"Found {count} unique names")

    logger.info("Grouping users by site")
    site_groups = {}
    for row in rows:
        full_name, title, site_name = row
        if site_name not in site_groups:
            site_groups[site_name] = []
        site_groups[site_name].append((full_name, title))

    logger.info("Building email body")
    email_body_html = "<html><body>"
    email_body_html += f"We have {count} users that used SafetyNet today as of {timestamp}.<br><br>"
    email_body_html += "Here's a list:<br><br>"

    for site_name, users in site_groups.items():
        email_body_html += f"<b>[{site_name}]</b><br>"
        for user in users:
            full_name, title = user
            email_body_html += f"{full_name} - {title}<br>"
        email_body_html += "<br><br>"

    email_body_html += "End of line.</body></html>"

    logger.info("Attaching email body to message")
    msg.attach(MIMEText(email_body_html, "html"))

    logger.info("Connecting to email server")
    server = smtplib.SMTP(credentials['email_server']['smtp_server'], credentials['email_server']['smtp_port'])
    server.starttls()
    logger.info("Logging in to email server")
    server.login(msg['From'], credentials['email_server']['password'])
    logger.info("Sending email")
    server.sendmail(msg['From'], [msg['To']] + msg['CC'].split(', ') if msg['CC'] else [], msg.as_string())
    logger.info("Email sent successfully")
    server.quit()
    logger.info("Exiting send_email function")