import json
import requests
import extract_mdl_selenium
from bs4 import BeautifulSoup


def extract_mdl_info():
    # URL der Seite mit den Informationen über die MdLs
    url = ('https://www.bayern.landtag.de/abgeordnete/abgeordnete-von-a-z/')

    # Eine GET-Anfrage an die URL senden
    response = requests.get(url)

    # BeautifulSoup verwenden, um das HTML der Seite zu analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Das ausgewählte Element der Filterung finden
    #selected_option = soup.find('option', {'selected': 'selected'}).text

    # Liste zum Speichern der gefundenen Informationen über die MdLs
    mdl_info_list = []

    '''# Selected auf alle ändern
    new_selected = "0"

    # Alle Optionen durchgehen und den "selected"-Wert anpassen
    for option in soup.find_all('option'):
        if option['value'] == new_selected:
            option['selected'] = 'selected'  # Neues "selected" setzen
        elif 'selected' in option.attrs:
            del option['selected']  # "selected" bei den anderen Optionen entfernen
'''
    # Tabelle mit den Informationen über die MdLs finden
    table = soup.find('table', class_='contenttable tx-stbltabgeordnete-table')

    # Durch die Zeilen der Tabelle iterieren und Informationen extrahieren
    rows = table.find_all('tr')
    for row in rows[1:]:  # Überspringe die Header-Zeile
        cols = row.find_all('td')
        if len(cols) >= 4:  # Überprüfe, ob alle benötigten Informationen vorhanden sind
            nachname = cols[1].text.strip()
            vorname = cols[2].text.strip()
            titel = cols[3].text.strip()
            fraktion = cols[4].text.strip()
            #email = cols[5].find('a')['href'].replace('mailto:', '').strip()
            if fraktion != 'AfD':
                mdl_info_list.append(
                    {'Nachname': nachname, 'Vorname': vorname, 'Titel': titel, 'Fraktion': fraktion}
                ) #, 'Email': email})
    return mdl_info_list


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
