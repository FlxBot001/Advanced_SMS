from django.db import models
from students.models import Student

class CocurricularActivity(models.Model):
    name = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    performance = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    supervisor = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Cocurricular activities'
        
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.name}" 