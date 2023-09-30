# Create your models here.

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} né le {self.birth_date} à {self.birth_place}"
