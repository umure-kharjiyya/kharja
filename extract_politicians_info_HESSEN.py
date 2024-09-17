import requests
from bs4 import BeautifulSoup
import string
import re


def extract_email_from_tag(tag):
    if tag:
        email_text = tag.get_text(strip=True)
        # Extrahiere E-Mail-Adresse aus dem Text
        email_match = re.search(r'\S+@\S+', email_text)
        return email_match.group(0) if email_match else None

def extract_mdl_info():
    base_url = 'https://hessischer-landtag.de'
    list_url = f'{base_url}/abgeordnete'
    mdl_info_list = []

    def get_detail_url(name_url):
        return f'{base_url}{name_url}'

    def clean_name(name):
        # Entfernen von Text in Klammern
        name = re.sub(r'\s*\(.*?\)\s*', '', name)
        # Namen trennen
        name_parts = name.split()
        if len(name_parts) >= 2:
            nachname = name_parts[-1]  # Der letzte Teil ist der Nachname
            vorname = ' '.join(name_parts[:-1])  # Der Rest ist der Vorname
        else:
            nachname = name
            vorname = ''
        return nachname, vorname

    # Iteriere durch alle Buchstaben von A bis Z
    for letter in string.ascii_uppercase:
        url = f'{list_url}?f%5B0%5D=abgeordnete_erster_buchstabe%3A{letter}'
        print(f'Abrufen der Daten für Buchstabe: {letter}')  # Debugging-Ausgabe

        # Eine GET-Anfrage an die URL senden
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Seite für Buchstabe {letter}: {response.status_code}")
            continue

        # BeautifulSoup verwenden, um das HTML der Seite zu analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finde alle Links zu den Detailseiten der Abgeordneten
        links = soup.select('a[href^="/abgeordnete/"]')
        if not links:
            print(f"Keine Links zu Detailseiten für Buchstabe {letter} gefunden.")
            continue

        for link in links:
            name = link.get_text(strip=True).replace("Bilddatei", "").strip()
            detail_url = get_detail_url(link['href'])

            # Hole die Detailseite des Abgeordneten
            detail_response = requests.get(detail_url)
            if detail_response.status_code != 200:
                print(f"Fehler beim Abrufen der Detailseite für {name}: {detail_response.status_code}")
                continue

            # BeautifulSoup verwenden, um das HTML der Detailseite zu analysieren
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            # Name auf der Detailseite finden
            name_tag = detail_soup.find('div',
                                        class_='field field--name-name field--type-name field--label-hidden field__item')
            if name_tag:
                full_name = name_tag.get_text(strip=True)
                # Überprüfen, ob es sich um ein Bild handelt
                if 'Bilddatei' in full_name:
                    print(f"Warnung: Bilddatei in Name für {detail_url}")
                    continue
                nachname, vorname = clean_name(full_name)
            else:
                nachname = 'Unbekannt'
                vorname = ''

            # Fraktion auf der Detailseite finden
            fraktion_tag = detail_soup.find('a', href=True, hreflang=True)
            if fraktion_tag:
                fraktion = fraktion_tag.get_text(strip=True)
            else:
                fraktion = 'Unbekannt'

            # E-Mail-Adresse auf der Detailseite finden
            email_tag = detail_soup.find('a', class_='spamspan')
            email = extract_email_from_tag(email_tag)

            # Speichern der Informationen in der Liste
            if fraktion not in ['Unbekannt', 'AfD', 'Alternative für Deutschland']:
                mdl_info_list.append({
                'Nachname': nachname,
                'Vorname': vorname,
                'Fraktion': fraktion,
                'Email': email
            })

    return mdl_info_list


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
