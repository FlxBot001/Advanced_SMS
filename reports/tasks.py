from celery import shared_task
from django.utils import timezone
from students.models import Student
from attendance.models import Attendance
from cocurricular.models import CocurricularActivity
from behavior.models import BehaviorRecord
from .utils import generate_pdf_report

@shared_task
def generate_monthly_reports():
    current_date = timezone.now().date()
    start_date = current_date.replace(day=1) - timezone.timedelta(days=1)
    end_date = current_date
    
    students = Student.objects.all()
    
    for student in students:
        attendance_records = Attendance.objects.filter(student=student, date__range=[start_date, end_date])
        cocurricular_activities = CocurricularActivity.objects.filter(student=student, date__range=[start_date, end_date])
        behavior_records = BehaviorRecord.objects.filter(student=student, date__range=[start_date, end_date])
        
        report_data = {
            'student': student,
            'attendance': attendance_records,
            'cocurricular': cocurricular_activities,
            'behavior': behavior_records,
            'start_date': start_date,
            'end_date': end_date,
        }
        
        pdf_report = generate_pdf_report(report_data)
        
        # Save the PDF report or send it via email
        # You can implement this part based on your specific requirements

