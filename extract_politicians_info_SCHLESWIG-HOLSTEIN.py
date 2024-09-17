import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_mdl_info():
    url = 'https://www.landtag.ltsh.de/abgeordnete/abgeordnete-alle/'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    mdl_info_list = []

    # Suche alle p-Tags, die sowohl Namen (in a-Tag) als auch Fraktionen enthalten
    p_tags = soup.find_all('p')

    for p_tag in p_tags:
        # Suche das a-Tag im p-Tag (Name)
        a_tag = p_tag.find('a')
        if a_tag:
            # Extrahiere den Namen
            name = a_tag.get_text(strip=True)

            # Extrahiere die Fraktion (nach dem Namen, in Klammern)
            text = p_tag.get_text(strip=True)
            if '(' in text and ')' in text:
                # Nimm den Text innerhalb der Klammern
                fraktion = text.split('(')[-1].split(')')[0]

                # Trenne Vor- und Nachnamen
                name_parts = name.split(', ')
                if len(name_parts) == 2:
                    nachname, vorname = name_parts
                else:
                    vorname = name_parts[0]
                    nachname = ""

                # Füge die Informationen zur Liste hinzu
                if 'AfD' not in fraktion and fraktion != 'Unbekannt':
                    mdl_info_list.append({
                    'Vorname': vorname,
                    'Nachname': nachname,
                    'Fraktion': fraktion
                })

    return mdl_info_list


def save_to_excel(data, file_name='mdl_info_landtag.xlsx'):
    # Konvertiere die Liste in ein pandas DataFrame
    df = pd.DataFrame(data)
    # Speichere die DataFrame in eine Excel-Datei
    df.to_excel(file_name, index=False)  # index=False, um die DataFrame-Indizes nicht als Spalte zu speichern


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    save_to_excel(mdl_info_list)
    print(f"{len(mdl_info_list)} Einträge gefunden.")
    for mdl_info in mdl_info_list:
        print(mdl_info)
