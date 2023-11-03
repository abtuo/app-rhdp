import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Initialisez le navigateur (assurez-vous que le pilote du navigateur approprié est installé)
driver = webdriver.Chrome()  # Exemple avec Chrome, utilisez le pilote de votre navigateur préféré

op = webdriver.ChromeOptions()
op.add_argument('headless')
#driver = webdriver.Chrome(options=op)
# Accédez à la page du site
driver.get('https://cei.ci/lep-23/')


def search_person_cei(name='DRAMANE', 
                  surname='OUATTARA', 
                  day='04', 
                  month='06', 
                  year='1964'
                  ):
    
    formulaire = driver.find_element(By.ID,  'formulaire')

    last_name_input = formulaire.find_element(By.NAME, 'nomfamille')
    first_name_input = formulaire.find_element(By.NAME, 'prenom')
    birth_day = formulaire.find_element(By.NAME, 'jour')

    birth_month = formulaire.find_element(By.NAME, 'mois')
    birth_year = formulaire.find_element(By.NAME, 'annee')

    time.sleep(2)
    day_dropdown = Select(birth_day)
    day_dropdown.select_by_value(day)

    month_dropdown = Select(birth_month)
    month_dropdown.select_by_value(month)

    year_dropdown = Select(birth_year)
    year_dropdown.select_by_value(year)
    first_name_input.send_keys(name)
    time.sleep(2)
    last_name_input.send_keys(surname)
    
    time.sleep(2)

    # Soumettez le formulaire
    search_button = formulaire.find_element(By.NAME,'search_cei_individu')
    search_button.click()
    time.sleep(3)

    result = driver.find_element(By.ID, 'resultat_electeur')

    result_dict = {line.split(' : ')[0]:line.split(' : ')[-1] for line in result.text.splitlines()}
    print(result_dict)

    time.sleep(5)

    # Fermer le navigateur
    driver.quit()
    return result_dict

import requests
from bs4 import BeautifulSoup
def person_on_cei() :
    
    NOM="DAO"
    PRENOM="BAZOUMANA"
    JOUR_DE_NAISSANCE="01"
    MOIS_DE_NAISSANCE = "04"
    ANNEE_DE_NAISSANCE="1995"

    the_data = f"nomfamille={NOM}&prenom={PRENOM}&jour={JOUR_DE_NAISSANCE}&mois={MOIS_DE_NAISSANCE}&annee={ANNEE_DE_NAISSANCE}&search_cei_individu=Lancer+la+recherche"
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

    print(RESULTATS)
    #print(RESULTATS['Département'])
    #print(RESULTATS_ELECTEURS)

if __name__ == '__main__':
    person_on_cei()
