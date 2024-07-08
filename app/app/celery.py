import os

from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

worker = Celery('app')

worker.config_from_object(f'django.conf:settings', namespace='CELERY')

worker.autodiscover_tasks()


@worker.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self!r}')
