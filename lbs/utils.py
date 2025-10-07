from django.core.mail import send_mail
from django.conf import settings


def send_enrollment_email(subject, core_message, book_title, user_email, start_date, end_date,admin_emails=None):

    message = (
            f"Hello,\n\n"
            f"{core_message}"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n\n"
            f"Thank you."
        )
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'library@example.com'

    recipients = [user_email]
    if admin_emails:
        recipients.extend(admin_emails)

    send_mail(subject, message, from_email, recipients)
