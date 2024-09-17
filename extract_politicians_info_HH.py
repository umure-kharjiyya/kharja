import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_mdl_info():
    base_url = 'https://www.hamburgische-buergerschaft.de/ueber-uns/abgeordneten-uebersicht'
    mdl_info_list = []

    # Sende eine GET-Anfrage an die Haupt-URL
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Hauptseite: {response.status_code}")
        return mdl_info_list

    # BeautifulSoup verwenden, um das HTML der Hauptseite zu analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finde alle Slider-Elemente für die Abgeordneten
    slider_elements = soup.find_all('div', class_='bkhh-member-slider__element')

    for element in slider_elements:
        card = element.find('div', class_='bkhh-member-card')
        if card:
            link_tag = card.find('a', class_='bkhh-link')
            name_tag = card.find('p', class_='bkhh-member-card__name')

            if link_tag and name_tag:
                # Extrahiere den Namen und den Link zur Detailseite
                name_text = name_tag.get_text(strip=True)
                profile_url = link_tag['href']
                full_profile_url = f"https://www.hamburgische-buergerschaft.de{profile_url}"

                # Trenne Vor- und Nachname
                name_parts = name_text.split()
                if len(name_parts) > 1:
                    first_name = " ".join(name_parts[:-1])  # Alles außer dem letzten Wort ist der Vorname
                    last_name = name_parts[-1]  # Das letzte Wort ist der Nachname
                else:
                    first_name = name_parts[0]
                    last_name = ''

                # Hole die Fraktion von der Profilseite
                fraktion = extract_fraktion(full_profile_url)

                # Füge die Daten zur Liste hinzu
                if 'AfD' not in fraktion and fraktion != 'Unbekannt':
                    mdl_info_list.append({
                        'Vorname': first_name,
                        'Nachname': last_name,
                        'Fraktion': fraktion
                    })

    return mdl_info_list

def extract_fraktion(profile_url):
    try:
        response = requests.get(profile_url)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Profilseite: {response.status_code}")
            return 'Unbekannt'

        soup = BeautifulSoup(response.text, 'html.parser')
        fraktion_tag = soup.find('div', class_='bkhh-profile-card__fraction')
        if fraktion_tag:
            x=fraktion_tag.get_text(strip=True)
            return x.split('-')[0] if "-Bürgerschaftsfraktion" in x else x
        return 'Unbekannt'
    except Exception as e:
        print(f"Fehler beim Abrufen der Fraktion: {e}")
        return 'Unbekannt'

def save_to_excel(data, file_name='mdl_info_hamburg.xlsx'):
    # Konvertiere die Liste von Dictionaries in ein pandas DataFrame
    df = pd.DataFrame(data)
    # Speichere das DataFrame als Excel-Datei
    df.to_excel(file_name, index=False)  # index=False, um das DataFrame-Index nicht als Spalte zu speichern

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    # save_to_excel(mdl_info_list)
    # print(len(mdl_info_list))
    for mdl_info in mdl_info_list:
        print(mdl_info)
