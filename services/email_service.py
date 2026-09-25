import smtplib
from email.message import EmailMessage

from core.config import settings
from core.logger import logger


def send_email_notification(subject: str, message_text: str, recipient: str | None = None) -> bool:
    """Send SMTP email notification with robust error logging and exception handling."""
    username = settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    clinic_email = recipient or settings.CLINIC_EMAIL

    if not all([host, username, password]):
        logger.warning(
            f"SMTP email notification skipped: Missing credentials (Host: {bool(host)}, User: {bool(username)})."
        )
        return False

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = username
    email["To"] = clinic_email
    email.set_content(message_text)

    try:
        logger.info(f"Connecting to SMTP server '{host}:{port}' to send email notification...")
        with smtplib.SMTP_SSL(host, int(port), timeout=10) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(email)
        logger.info(f"Successfully sent email notification to '{clinic_email}' with subject '{subject}'")
        return True
    except smtplib.SMTPAuthenticationError as exc:
        logger.error(f"SMTP authentication failed for user '{username}': {exc}")
        return False
    except smtplib.SMTPException as exc:
        logger.error(f"SMTP protocol error when sending notification: {exc}", exc_info=True)
        return False
    except Exception as exc:
        logger.error(f"Unexpected error when sending email notification: {exc}", exc_info=True)
        return False
