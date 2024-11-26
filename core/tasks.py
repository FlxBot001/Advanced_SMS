from celery import shared_task
from .report_generator import generate_student_report
from students.models import Student
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def generate_student_reports():
    students = Student.objects.all()
    for student in students:
        pdf = generate_student_report(student)
        filename = f"student_report_{student.student_id}.pdf"
        path = default_storage.save(f"reports/{filename}", ContentFile(pdf))
        
def send_email_task(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

@shared_task
def generate_report_task(report_type, user_id):
    # Implement report generation logic here
    pass

