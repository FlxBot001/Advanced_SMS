from django.db import models
from core.models import Person

class Parent(Person):
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - Parent"

