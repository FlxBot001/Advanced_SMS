from django.db import models
from core.models import BaseModel
from teachers.models import Teacher
from students.models import Student

class Subject(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    learning_area = models.CharField(max_length=100)  # e.g., Languages, Mathematics, Sciences
    grade_level = models.CharField(max_length=50)     # e.g., Grade 1, Grade 2
    
    def __str__(self):
        return f"{self.name} - {self.code}"

class Strand(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='strands')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class SubStrand(BaseModel):
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='sub_strands')
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.strand.name} - {self.name}"

class LearningOutcome(BaseModel):
    sub_strand = models.ForeignKey(SubStrand, on_delete=models.CASCADE, related_name='learning_outcomes')
    description = models.TextField()
    assessment_criteria = models.TextField()
    
    def __str__(self):
        return f"{self.sub_strand.name} - Outcome"

class Course(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses')
    is_default = models.BooleanField(default=False)
    term = models.CharField(max_length=20)  # e.g., Term 1, Term 2, Term 3
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.code}"

class CourseDocument(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_documents/')

    def __str__(self):
        return f"{self.course.name} - {self.title}"

