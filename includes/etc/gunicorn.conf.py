import logging
import os

from pathlib import Path

from django.conf import settings

from prometheus_client import CollectorRegistry, multiprocess, start_http_server



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

access_logfile = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({x-forwarded-for}i)s"'

bind = 'unix:/run/gunicorn.sock'

forwarded_allow_ips = "*"
forwarder_headers = "X-REAL-IP,X-FORWARDED-FOR,X-FORWARDED-PROTO"

logger = logging.getLogger(__name__)

preload_app = False

workers = 10


def when_ready(_):

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


def child_exit(_, worker):

    multiprocess.mark_process_dead(worker.pid)
