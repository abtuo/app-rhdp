from django.shortcuts import render

# Create your views here.

# myapp/views.py

from django.shortcuts import render
from .models import Person

def search_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        person = None

        if first_name and last_name:
            try:
                person = Person.objects.get(first_name=first_name, last_name=last_name)
            except Person.DoesNotExist:
                pass

        return render(request, 'search_result.html', {'person': person})

    return render(request, 'search_form.html')
