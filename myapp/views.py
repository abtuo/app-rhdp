from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm

# Create your views here.

# myapp/views.py

from django.shortcuts import render
from .models import Person
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#from .scrap_cei import search_person_cei
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
# Accédez à la page du site
driver.get('https://cei.ci/lep-23/')


def search_person_cei(request,
                  name='DRAMANE', 
                  surname='OUATTARA', 
                  day='04', 
                  month='06', 
                  year='1964'
                  ):
    
    if request.method == 'POST':
    
        formulaire = driver.find_element(By.ID,  'formulaire')

        last_name_input = formulaire.find_element(By.NAME, 'nomfamille')
        first_name_input = formulaire.find_element(By.NAME, 'prenom')
        birth_day = formulaire.find_element(By.NAME, 'jour')

        birth_month = formulaire.find_element(By.NAME, 'mois')
        birth_year = formulaire.find_element(By.NAME, 'annee')

        day_dropdown = Select(birth_day)
        day_dropdown.select_by_value(day)

        month_dropdown = Select(birth_month)
        month_dropdown.select_by_value(month)

        year_dropdown = Select(birth_year)
        year_dropdown.select_by_value(year)
        # Remplissez les champs du formulaire
        first_name_input.send_keys(name)
        last_name_input.send_keys(surname)
 
        # Soumettez le formulaire
        search_button = formulaire.find_element(By.NAME,'search_cei_individu')
        search_button.click()

        result = driver.find_element(By.ID, 'resultat_electeur')


        result_dict = {line.split(' : ')[0]:line.split(' : ')[-1] for line in result.text.splitlines()}

        # Fermer le navigateur
        driver.quit()
        return render(request, 'search_form_cei.html', {'result_dict': result_dict})

    return render(request, 'search_form_cei.html', {})
   

def search_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        person = None

        if first_name and last_name:
            try:
                person = Person.objects.get(first_name=first_name, last_name=last_name)
            except Person.DoesNotExist:
                #person = f"{first_name} {last_name}"
                pass

            #person_on_cei = search_person_cei(name=first_name, surname=last_name)
            #if len(person_on_cei) <= 2:
            #    person_on_cei = None

        return render(request, 'search_result.html', {'person': person})

    return render(request, 'search_form.html')

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                # Essayez d'ajouter la personne à la base de données
                form.save()
                # Réinitialisez le formulaire
                form = PersonForm()
                success = True
                error_message = None
            except IntegrityError:
                # Si la personne existe déjà dans la base de données
                success = False
                error_message = "La personne existe déjà dans la base de données."
        else:
            success = False
            error_message = "Le formulaire n'est pas valide."
    else:
        form = PersonForm()
        success = False
        error_message = None
    return render(request, 'add_person.html', {'form': form, 'success': success, 'error_message': error_message})


def view_all_persons(request):
    persons = Person.objects.all()
    return render(request, 'all_persons.html', {'persons': persons})
