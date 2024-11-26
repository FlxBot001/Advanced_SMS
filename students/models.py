from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from core.models import Person

class Student(Person):
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    enrollment_date = models.DateField(default=timezone.now)
    graduation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new student
            self.graduation_date = self.enrollment_date + relativedelta(years=7)
        super().save(*args, **kwargs)

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    year = models.IntegerField()

    class Meta:
        unique_together = ('student', 'subject', 'year')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject} - {self.year}"



class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

