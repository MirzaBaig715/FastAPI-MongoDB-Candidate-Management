from celery import Celery

from src.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "src.services.tasks.*": {"queue": "main-queue"}
}
