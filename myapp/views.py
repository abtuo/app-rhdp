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

import requests
from bs4 import BeautifulSoup

#from .scrap_cei import search_person_cei
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
# Accédez à la page du site
driver.get('https://cei.ci/lep-23/')


def search_person_cei(name='DRAMANE', 
                  surname='OUATTARA', 
                  day='04', 
                  month='06', 
                  year='1964'
                  ):
    
    the_data = f"nomfamille={surname}&prenom={name}&jour={day}&mois={month}&annee={year}&search_cei_individu=Lancer+la+recherche"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post("https://cei.ci/liste-electorale-definitive-2023/", data=the_data, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    #nom = soup.body.div.div.div.section[3].div.div.div.div.div
    RESULTATS_ELECTEURS = (soup.select("div.elementor-shortcode")[1]).select('h6')

    RESULTATS = {}
    for res in RESULTATS_ELECTEURS:
        #print(res.text)
        KEY = (((res.text).split(":"))[0]).strip()
        try : 
            VALUE = (((res.text).split(":"))[1]).strip()
        except: 
            VALUE = ""
        RESULTATS[KEY] = VALUE
    return RESULTATS


def search_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        birth_date = request.POST.get('birth_date')
        year, month, day = birth_date.split('-')


        if first_name and last_name:
            try:
                person = Person.objects.get(first_name=first_name, 
                                            last_name=last_name, 
                                            birth_date=birth_date, 
                                            )
                person_in_db = True
            except Person.DoesNotExist:
                person_in_db = False
                person = f"{first_name} {last_name}"
                pass

            person_on_cei = search_person_cei(name=first_name, 
                                              surname=last_name,
                                              day=day,
                                              month=month,
                                              year=year
                                              )
            
            no_electeur = person_on_cei.get("Numéro d'électeur", None)
            centre_vote = person_on_cei.get("Lieu de vote", None)

            nom = person_on_cei.get("Nom", None)
            prenom = person_on_cei.get("Prénom", None)

            if len(person_on_cei) <= 2:
                person_on_cei = None
            elif nom and prenom:
                person_on_cei = f"{nom} {prenom}"

            return render(request, 'search_result.html', {'person': person, 'person_in_db': person_in_db, 'person_on_cei': person_on_cei, 'no_electeur': no_electeur, 'centre_vote': centre_vote})

    return render(request, 'search_form.html')

def search_result(request):

    return render(request, 'search_result.html')

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
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
        form = PersonForm()
        success = False
        error_message = None

    return render(request, 'add_person.html', {'form': form, 'success': success, 'error_message': error_message})


def view_all_persons(request):
    persons = Person.objects.all()
    return render(request, 'all_persons.html', {'persons': persons})
