from django.db import models
from core.models import BaseModel

class Assessment(BaseModel):
    ASSESSMENT_TYPES = (
        ('formative', 'Formative Assessment'),
        ('summative', 'Summative Assessment'),
        ('project', 'Project Based Assessment'),
    )
    
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    learning_outcome = models.ForeignKey('courses.LearningOutcome', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    due_date = models.DateTimeField()

class StudentAssessment(BaseModel):
    COMPETENCY_LEVELS = (
        ('exceeding', 'Exceeding Expectations'),
        ('meeting', 'Meeting Expectations'),
        ('approaching', 'Approaching Expectations'),
        ('below', 'Below Expectations'),
    )
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    competency_level = models.CharField(max_length=20, choices=COMPETENCY_LEVELS)
    teacher_feedback = models.TextField()
    evidence = models.FileField(upload_to='assessment_evidence/', null=True, blank=True) 