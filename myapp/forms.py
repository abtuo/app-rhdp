# myapp/forms.py

from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 
                  'last_name', 
                  'birth_date', 
                  'sexe', 
                  'contact', 
                  'section', 
                  'city', 
                  'country',
                  'is_on_cei']