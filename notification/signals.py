from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course
from .models import Notification

@receiver(post_save, sender=Course)
def create_course_notification(sender, instance, created, **kwargs):
    if created:
        students = instance.students.all()
        for student in students:
            Notification.objects.create(
                user=student.user,
                message=f"New course assigned: {instance.name}"
            )

