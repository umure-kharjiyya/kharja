import requests
from bs4 import BeautifulSoup
import string


def extract_mdl_info():
    base_url = 'https://www.bayern.landtag.de/abgeordnete/abgeordnete-von-a-z/'
    mdl_info_list = []

    # Iteriere durch alle Buchstaben von A bis Z
    for letter in string.ascii_uppercase:
        url = f'{base_url}?tx_stbltabgeordnete_filter%5Bletter%5D={letter}&tx_stbltabgeordnete_filter%5Bperiod-time%5D=a'
        print(f'Abrufen der Daten für Buchstabe: {letter}')  # Debugging-Ausgabe

        # Eine GET-Anfrage an die URL senden
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Seite für Buchstabe {letter}: {response.status_code}")
            continue

        # BeautifulSoup verwenden, um das HTML der Seite zu analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tabelle mit den Informationen über die MdLs finden
        table = soup.find('table', class_='contenttable tx-stbltabgeordnete-table')

        if not table:
            print(f"Keine Tabelle für Buchstabe {letter} gefunden.")
            continue

        # Durch die Zeilen der Tabelle iterieren und Informationen extrahieren
        rows = table.find_all('tr')
        for row in rows[1:]:  # Überspringe die Header-Zeile
            cols = row.find_all('td')
            if len(cols) >= 4:  # Überprüfe, ob alle benötigten Informationen vorhanden sind
                nachname = cols[1].text.strip()
                vorname = cols[2].text.strip()
                titel = cols[3].text.strip()
                fraktion = cols[4].text.strip()

                if fraktion != 'AfD' and fraktion != 'Alternative für Deutschland':  # AfD-Abgeordnete ausschließen
                    mdl_info_list.append({
                        'Nachname': nachname,
                        'Vorname': vorname,
                        'Titel': titel,
                        'Fraktion': fraktion
                    })

    return mdl_info_list


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
