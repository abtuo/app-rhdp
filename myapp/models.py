# Create your models here.

from django.db import models


# models.py

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    
    sexe = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'birth_date'], name='unique_name')
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name} né le {self.birth_date}"


class PersonCEI(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} né le {self.birth_date}"
