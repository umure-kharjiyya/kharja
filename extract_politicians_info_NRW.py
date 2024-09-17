import requests
from bs4 import BeautifulSoup
import string

def extract_mdl_info():
    base_url = 'https://www.landtag.nrw.de/home/der-landtag/abgeordnete-und--fraktionen/die-abgeordneten/abgeordnetensuche/suche-nach-alphabet.html'
    mdl_info_list = []

    # Iteriere durch alle Buchstaben von A bis Z
    for letter in string.ascii_uppercase:
        url = f'{base_url}?letter={letter}'
        print(f'Abrufen der Daten für Buchstabe: {letter}')  # Debugging-Ausgabe

        # Eine GET-Anfrage an die URL senden
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Seite für Buchstabe {letter}: {response.status_code}")
            continue

        # BeautifulSoup verwenden, um das HTML der Seite zu analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finde alle Zeilen mit Abgeordneteninformationen (tr-Tags)
        rows = soup.find_all('tr')

        # Durch die Zeilen iterieren und die Informationen extrahieren
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:  # Überprüfe, ob alle benötigten Informationen vorhanden sind
                # Namen des Abgeordneten im ersten td->a Tag
                name_tag = cols[0].find('a')
                name = name_tag.text.strip() if name_tag else cols[0].text.strip()

                # Trennen von Nachname und Vorname (erster Teil ist Nachname, Rest ist Vorname)
                name_parts = name.split()
                if len(name_parts) >= 2:
                    nachname = name_parts[0]  # Das erste Wort ist der Nachname
                    vorname = ' '.join(name_parts[1:])  # Der Rest ist der Vorname
                else:
                    nachname = name
                    vorname = ''

                # Fraktion des Abgeordneten im zweiten td->abbr Tag
                fraktion_tag = cols[1].find('abbr')
                fraktion = fraktion_tag['title'] if fraktion_tag else cols[1].text.strip()

                # Speichern der Informationen in der Liste, AfD-Abgeordnete ausschließen
                if fraktion not in ['AfD', 'Alternative für Deutschland']:
                    mdl_info_list.append({
                        'Nachname': nachname,
                        'Vorname': vorname,
                        'Fraktion': fraktion
                    })

    return mdl_info_list

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
