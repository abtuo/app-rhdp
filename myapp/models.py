# models.py
from bs4 import BeautifulSoup

from django.db import models
import requests

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
    
    if len(RESULTATS)<=2:
        RESULTATS = False
    else:
        RESULTATS = True
    return RESULTATS


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    
    sexe = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    on_cei = False
    is_on_cei = models.BooleanField(default=on_cei)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'birth_date'], name='unique_name')
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name} né(e) le {self.birth_date}"


class PersonCEI(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} né(e) le {self.birth_date}"
