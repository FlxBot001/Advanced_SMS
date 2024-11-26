from django.core.management.base import BaseCommand
from django.utils import timezone
from clearance.models import ClearanceRequest

class Command(BaseCommand):
    help = 'Cleanup expired clearance requests'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = ClearanceRequest.objects.filter(
            end_time__lt=now,
            status=ClearanceRequest.Status.APPROVED
        )
        count = expired.update(status=ClearanceRequest.Status.EXPIRED)
        self.stdout.write(f"Expired {count} clearance requests") 