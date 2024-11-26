from django.db import models
from students.models import Student

class BehaviorRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    is_positive = models.BooleanField(default=True)
    points = models.IntegerField(default=0)
    recorded_by = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date}" 