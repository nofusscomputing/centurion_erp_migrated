import logging
import os

from django.conf import settings

from celery import Celery, signals
from celery.fixups.django import DjangoFixup

from pathlib import Path

from prometheus_client import CollectorRegistry, multiprocess, start_http_server

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

worker = Celery('app')

worker.config_from_object(f'django.conf:settings', namespace='CELERY')

worker.autodiscover_tasks()


@worker.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self!r}')



@signals.worker_ready.connect()
def setup_prometheus(**kwargs):

    if not getattr(settings, 'METRICS_ENABLED', False):
        return

    proc_path = None

    try:
        proc_path = os.environ["PROMETHEUS_MULTIPROC_DIR"]
    except:
        pass


    if not proc_path:

        os.environ["PROMETHEUS_MULTIPROC_DIR"] = settings.METRICS_MULTIPROC_DIR

        proc_path = os.environ["PROMETHEUS_MULTIPROC_DIR"]


    logger.info(f'Setting up prometheus metrics HTTP server on port {str(settings.METRICS_EXPORT_PORT)}.')

    multiproc_folder_path = _setup_multiproc_folder()

    registry = CollectorRegistry()

    logger.info(f'Setting up prometheus metrics directory.')

    multiprocess.MultiProcessCollector(registry, path=multiproc_folder_path)

    logger.info(f'Starting prometheus metrics server.')

    start_http_server( settings.METRICS_EXPORT_PORT, registry=registry)

    logger.info(f'Starting prometheus serving on port {str(settings.METRICS_EXPORT_PORT)}.')



def _setup_multiproc_folder():

    coordination_dir = Path(os.environ["PROMETHEUS_MULTIPROC_DIR"])

    coordination_dir.mkdir(parents=True, exist_ok=True)

    for filepath in coordination_dir.glob("*.db"):

        filepath.unlink()

    return coordination_dir
