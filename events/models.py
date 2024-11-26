from django.db import models
from teachers.models import Teacher
from courses.models import Course

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    is_school_wide = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return f"{self.title} - {self.date.date()}" 