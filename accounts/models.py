from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )

    ROLE_CHOICES = [
        ('principal', 'Principal'),
        ('deputy_principal', 'Deputy Principal'),
        ('senior_teacher', 'Senior Teacher'),
        ('department_head', 'Department Head'),
        ('class_teacher', 'Class Teacher'),
        ('lab_technician', 'Lab Technician'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('student_leader', 'Student Leader'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    national_id = models.IntegerField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.username