from django.db import models
django.contrib.auth import get_user_model
from students.models import Student

# Create your models here.

class Attendance(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    