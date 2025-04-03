from celery import Celery

from common.config import get_rabbitmq_settings
from common.constants import CELERY_WORKER_NAME

celery_app = Celery(
    CELERY_WORKER_NAME,
    broker=get_rabbitmq_settings().get_url(),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["worker.tasks"])
