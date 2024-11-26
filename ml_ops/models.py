from django.db import models
from students.models import Student

class StudentPrediction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    predicted_score = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - {self.predicted_score}"

