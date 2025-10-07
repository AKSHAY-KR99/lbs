import os
from celery import Celery
from celery.schedules import crontab  # for scheduling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')

app = Celery('library_management_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-expired-enrollments-midnight': {
        'task': 'lbs.tasks.check_expired_enrollments',
        'schedule': crontab(minute='*/2')

    },
}

app.conf.timezone = 'Asia/Kolkata'
