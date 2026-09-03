from celery import Celery
from src.core.config import settings

celery_app = Celery(
    "search_platform",
    broker=settings.celery_broker_url,
    backend=settings.redis_url,
    include=["src.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1, # Important for large tasks
    task_acks_late=True, # Ensure we don't drop tasks on crash
    broker_connection_retry_on_startup=True
)
