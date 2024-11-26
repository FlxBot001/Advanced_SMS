from celery import shared_task
from django.utils import timezone
from .models import Attendance
from notifications.utils import send_notification

@shared_task
def send_daily_attendance_messages():
    today = timezone.now().date()
    attendances = Attendance.objects.filter(date=today, is_present=False)
    
    for attendance in attendances:
        student = attendance.student
        parent = student.parents.first()  # Assuming a student can have multiple parents
        if parent:
            message = f"Your child {student.user.get_full_name()} was absent from school today."
            send_notification(parent.user, message, related_object=attendance)

