from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from .models import ClearanceRequest, ClearanceLog

@receiver(post_save, sender=ClearanceRequest)
def handle_clearance_status_change(sender, instance, created, **kwargs):
    if created:
        ClearanceLog.objects.create(
            clearance=instance,
            action=ClearanceLog.ActionType.CREATED,
            performed_by=instance.user
        )
        # Notify approvers
        notify_approvers(instance)
    else:
        # Check for status changes and handle accordingly
        if instance.status == ClearanceRequest.Status.APPROVED:
            schedule_expiration(instance)
        elif instance.status == ClearanceRequest.Status.REJECTED:
            notify_user_of_rejection(instance)

def notify_approvers(clearance):
    # Implementation for notifying approvers
    pass

def schedule_expiration(clearance):
    # Implementation for scheduling expiration
    pass 