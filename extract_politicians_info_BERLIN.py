import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_mdl_info():
    base_url = 'https://www.parlament-berlin.de/das-parlament/abgeordnete/alphabetische-suche'
    mdl_info_list = []

    # Sende eine GET-Anfrage an die Haupt-URL
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Hauptseite: {response.status_code}")
        return mdl_info_list

    # BeautifulSoup verwenden, um das HTML der Hauptseite zu analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finde alle Sektionen für die Buchstaben
    sections = soup.find_all('basic-toggle')
    for section in sections:
        # Extrahiere den Buchstaben, der die Sektion beschreibt
        header = section.find('h2', class_='text-title')
        if header:
            letter = header.get_text(strip=True)
            print(f"Verarbeite Buchstabe: {letter}")

        # Finde alle Listeneinträge innerhalb der Sektion
        list_items = section.find_all('li', class_='linklist-item')
        for item in list_items:
            link = item.find('a')
            if link:
                # Extrahiere den vollständigen Text
                text = link.get_text(strip=True)
                # Versuche verschiedene Trennzeichen
                for delimiter in ['Fraktion']:
                    if delimiter in text:
                        name_part, fraktion = text.split(',', 1)
                        # Name trennen in Nachname und Vorname
                        name_parts = name_part.split(', ')
                        if len(name_parts) == 2:
                            nachname = name_parts[0].strip()
                            vorname = name_parts[1].strip()
                        else:
                            nachname = name_part.strip()
                            vorname = ''

                        # Filtern der AfD-Abgeordneten
                        if 'AfD' not in fraktion:
                            mdl_info_list.append({
                                'Nachname': nachname,
                                'Vorname': vorname,
                                'Fraktion': fraktion.strip()
                            })
                        break  # Breche die Schleife ab, wenn der Trennzeichen gefunden wurde

    return mdl_info_list

def save_to_excel(data, file_name='mdl_info.xlsx'):
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    # Save DataFrame to an Excel file
    df.to_excel(file_name, index=False)  # index=False to avoid saving the DataFrame index as a column

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    save_to_excel(mdl_info_list)
    for mdl_info in mdl_info_list:
        print(mdl_info)
