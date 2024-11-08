from celery import shared_task

from src.services.candidate_service import CandidateService


@shared_task
def generate_report_task():
    """Background task to generate candidate report."""
    service = CandidateService()
    return service.generate_report()


@shared_task
def send_notification_task(email: str, subject: str, message: str):
    """Background task to send notifications."""
    pass
