from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from courses.models import Course

@receiver(post_save, sender=Student)
def assign_default_courses(sender, instance, created, **kwargs):
    if created:
        default_courses = Course.objects.filter(is_default=True)
        instance.courses.add(*default_courses)

