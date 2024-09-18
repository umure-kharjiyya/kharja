import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_mdl_info():
    url = 'https://www.landtag-saar.de/abgeordnete-und-fraktionen/abgeordnete/'

    # Abrufen der Hauptseite mit den Abgeordneten
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    mdl_info_list = []

    # Finde alle Abgeordneten-Container
    members_containers = soup.find_all('div', class_='ltContainerItem')

    for member in members_containers:
        # Name des Abgeordneten extrahieren
        name_tag = member.find('h4', class_='ProfileName')
        full_name = name_tag.get_text(strip=True) if name_tag else 'Unbekannt'

        # Fraktion extrahieren (aus dem alt-Attribut des img-Tags innerhalb des fraction-logo-wrapper)
        fraktion_tag = member.find('div', class_='fraction-logo-wrapper').find('img')
        fraktion = fraktion_tag.get('alt') if fraktion_tag else 'Unbekannt'

        # E-Mail (nicht verfügbar, aber JavaScript Aufruf anzeigen)
        email_tag = member.find('a', onclick=True)
        if email_tag:
            email = email_tag.get_text(strip=True)
            if '@' in email:  # check if email address is valid
                pass
            else:
                email = None

            # Namen aufteilen
        names_parts = full_name.split(' ')
        if len(names_parts) >= 2:
            vorname = ' '.join(names_parts[:-1]).strip()
            nachname = names_parts[-1].strip()
        else:
            vorname = names_parts[0].strip()
            nachname = ""

        # Ergebnisse zur Liste hinzufügen
        if 'AFD' not in fraktion and fraktion != 'Unbekannt':
            mdl_info_list.append({
            'Nachname': nachname,
            'Vorname': vorname,
            'Fraktion': fraktion,
            'Email': email
        })

    return mdl_info_list


def save_to_excel(data, file_name='mdl_info_saarland.xlsx'):
    # Konvertiere die Liste in ein pandas DataFrame
    df = pd.DataFrame(data)
    # Speichere die Daten in eine Excel-Datei
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    if mdl_info_list:
        # Daten in eine Excel-Datei speichern
        save_to_excel(mdl_info_list)
        print(f"{len(mdl_info_list)} Einträge gefunden.")
    else:
        print("Keine Einträge gefunden.")
