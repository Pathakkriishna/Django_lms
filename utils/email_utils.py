# utils/email_utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    """
    Sends an email notification.
    :param subject: Email subject line
    :param message: Email body text
    :param recipient_list: List of recipient email addresses
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Sender address from settings.py
        recipient_list,
        fail_silently=False
    )
