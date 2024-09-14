import requests
from bs4 import BeautifulSoup
import string

def extract_mdl_info():
    base_url = 'https://www.landtag.nrw.de'
    search_url = f'{base_url}/home/der-landtag/abgeordnete-und--fraktionen/die-abgeordneten/abgeordnetensuche/suche-nach-alphabet.html?letter='

    mdl_info_list = []

    # Iteriere durch alle Buchstaben von A bis Z
    for letter in string.ascii_uppercase:
        url = f'{search_url}{letter}&tx_stbltabgeordnete_filter%5Bperiod-time%5D=a'

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page for letter {letter}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Die Tabelle der Abgeordneten finden
        table = soup.find('table', class_='contenttable')  # Ersetze 'contenttable' durch die korrekte Klassenbezeichnung

        if table:
            rows = table.find_all('tr')  # Alle Zeilen der Tabelle durchsuchen

            for row in rows[1:]:  # Die erste Zeile überspringen, weil sie oft die Header ist
                cols = row.find_all('td')  # Finde alle Spalten (td-Tags) in der Zeile

                if len(cols) >= 2:
                    # Beispiel: Name könnte im ersten td-Tag sein
                    name_tag = cols[0].find('a')  # Den Link für den Namen finden
                    name = name_tag.text.strip() if name_tag else cols[0].text.strip()  # Name extrahieren

                    # Fraktion könnte im zweiten td-Tag sein
                    fraktion_tag = cols[1].find('abbr')  # Den abbr-Tag für die Fraktion finden
                    fraktion = fraktion_tag['title'] if fraktion_tag else cols[1].text.strip()  # Fraktion extrahieren

                    mdl_info_list.append({
                        'Name': name,
                        'Fraktion': fraktion
                    })

    return mdl_info_list

