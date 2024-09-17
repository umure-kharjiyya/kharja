import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_mdl_info():
    url = 'https://www.landtag-mv.de/landtag/abgeordnete/name'  # Placeholder for the actual page URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    mdl_info_list = []

    # Suche alle 'letterGroup' divs, die die Informationen enthalten
    letter_groups = soup.find_all('div', class_='frame frame-default frame-type-list frame-layout-0')

    for group in letter_groups:
        # Suche alle tr-Tags in der Tabelle
        rows = group.find_all('tr')

        for row in rows:
            # Hole den Namen (im a-Tag innerhalb des ersten td-Tags)
            name_td = row.find('td')
            if name_td:
                name = name_td.get_text(strip=True)
                names_parts = name.split(' ')
                vorname =(' ').join(names_parts[:-1])
                nachname = names_parts[-1]

                # Hole die Fraktion aus dem zweiten td-Tag
                fraktion_td = row.find_all('td')[1]
                fraktion = fraktion_td.get_text(strip=True)

                # Füge die Daten zur Liste hinzu
                if 'AfD' not in fraktion:
                    mdl_info_list.append({
                    'Name': nachname,
                    'Vorname': vorname,
                    'Fraktion': fraktion
                })

    return mdl_info_list

def save_to_excel(data, file_name='mdl_info_mv_landtag.xlsx'):
    # Konvertiere die Liste in ein pandas DataFrame
    df = pd.DataFrame(data)
    # Speichere die DataFrame in eine Excel-Datei
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    # save_to_excel(mdl_info_list)
    print(f"{len(mdl_info_list)} Einträge gefunden.")
    for mdl_info in mdl_info_list:
        print(mdl_info)
        print(mdl_info)
