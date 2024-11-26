from celery import shared_task
from django.utils import timezone
from .models import ClearanceRequest

@shared_task
def check_expired_clearances():
    now = timezone.now()
    expired = ClearanceRequest.objects.filter(
        status=ClearanceRequest.Status.APPROVED,
        end_time__lt=now
    )
    for clearance in expired:
        clearance.status = ClearanceRequest.Status.EXPIRED
        clearance.save()

@shared_task
def send_clearance_reminders():
    # Send reminders for expiring clearances
    soon = timezone.now() + timezone.timedelta(days=1)
    expiring = ClearanceRequest.objects.filter(
        status=ClearanceRequest.Status.APPROVED,
        end_time__lt=soon
    )
    for clearance in expiring:
        notify_expiring_clearance(clearance) 