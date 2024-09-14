import requests
from bs4 import BeautifulSoup
import string  # Für die Buchstaben von A bis Z


def extract_mdl_info():
    base_url = 'https://www.bayern.landtag.de/abgeordnete/abgeordnete-von-a-z/?tx_stbltabgeordnete_filter%5Bletter%5D='

    # Liste zum Speichern der Informationen über alle MdLs
    mdl_info_list = []

    # Iteriere durch alle Buchstaben von A bis Z
    for letter in string.ascii_uppercase:
        url = f'{base_url}{letter}&tx_stbltabgeordnete_filter%5Bperiod-time%5D=a'

        try:
            # Eine GET-Anfrage an die URL senden
            response = requests.get(url)
            response.raise_for_status()  # Fehlerprüfung bei der Anfrage
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page for letter {letter}: {e}")
            continue  # Weiter zum nächsten Buchstaben

        # BeautifulSoup verwenden, um das HTML der Seite zu analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tabelle mit den Informationen über die MdLs finden
        table = soup.find('table', class_='contenttable tx-stbltabgeordnete-table')
        if not table:
            print(f"No table found for letter {letter}")
            continue  # Weiter zum nächsten Buchstaben

        # Durch die Zeilen der Tabelle iterieren und Informationen extrahieren
        rows = table.find_all('tr')
        for row in rows[1:]:  # Überspringe die Header-Zeile
            cols = row.find_all('td')
            if len(cols) >= 4:  # Überprüfe, ob alle benötigten Informationen vorhanden sind
                nachname = cols[1].text.strip()
                vorname = cols[2].text.strip()
                titel = cols[3].text.strip()
                fraktion = cols[4].text.strip()

                # Versuchen, die E-Mail zu finden, falls vorhanden
                email_link = cols[5].find('a') if len(cols) > 5 else None
                email = email_link['href'].replace('mailto:', '').strip() if email_link else None

                mdl_info_list.append(
                    {
                        'Nachname': nachname,
                        'Vorname': vorname,
                        'Titel': titel,
                        'Fraktion': fraktion,
                        'Email': email
                    }
                )

    return mdl_info_list

#print(extract_mdl_info())