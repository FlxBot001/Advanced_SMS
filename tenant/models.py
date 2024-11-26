from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class School(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SchoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.school.name}"

