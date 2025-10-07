from celery import shared_task
from django.utils import timezone
from .models import Enrollment
from django.contrib.auth import get_user_model
from .utils import send_enrollment_email

User = get_user_model()

@shared_task
def check_expired_enrollments():
    now = timezone.now()
    expired = Enrollment.objects.filter(end_date__lt=now, status='ENROLLED')
    for enrollment in expired:
        enrollment.status = 'EXPIRED'
        enrollment.save()

        book = enrollment.book
        book.is_available = True
        book.save()
        admin_emails = list(User.objects.filter(role='ADMIN').values_list('email', flat=True))
        print("task scheduler ----------> ")
        send_enrollment_email(
            subject=f"Book Enrollment Expired: {enrollment.book.title}",
            core_message=f"The book '{enrollment.book.title}' was expired on today\n",
            book_title=enrollment.book.title,
            user_email=enrollment.user.email,
            start_date=enrollment.start_date,
            end_date=enrollment.end_date,
            admin_emails=admin_emails
        )
