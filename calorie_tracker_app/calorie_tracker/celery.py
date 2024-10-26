import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calorie_tracker.settings')

app = Celery('calorie_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'convert_pdf_and_send': {
        'task': 'convert_pdf_and_send',
        'schedule': crontab(minute='*/2'),  
    }
}


