import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

# Funktion zum Extrahieren der MdL-Informationen
def extract_mdl_info():
    # Starte den Webdriver (angenommen, du nutzt Chrome)
    driver = webdriver.Chrome()

    # Öffne die Webseite
    driver.get('https://www.bayern.landtag.de/abgeordnete/abgeordnete-von-a-z/')

    # Warte, bis die Dropdown-Liste sichtbar ist und interagiert werden kann
    time.sleep(3)  # Warte, damit die Seite vollständig geladen wird

    # Finde das Dropdown-Menü für die Trefferanzahl und setze es auf "alle"
    dropdown = Select(driver.find_element(By.NAME, 'tx_stbltabgeordnete_filter[perpage]'))
    dropdown.select_by_value('0')  # '0' scheint der Wert für "alle" zu sein

    # Warte, damit die Seite nach der Auswahl neu geladen wird
    time.sleep(5)

    # Extrahiere die HTML-Seite nach der Interaktion
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Tabelle mit den Informationen über die MdLs finden
    table = soup.find('table', class_='contenttable tx-stbltabgeordnete-table')

    # Liste zum Speichern der gefundenen Informationen über die MdLs
    mdl_info_list = []

    # Durch die Zeilen der Tabelle iterieren und Informationen extrahieren
    rows = table.find_all('tr')
    for row in rows[1:]:  # Überspringe die Header-Zeile
        cols = row.find_all('td')
        if len(cols) >= 4:  # Überprüfe, ob alle benötigten Informationen vorhanden sind
            nachname = cols[1].text.strip()
            vorname = cols[2].text.strip()
            titel = cols[3].text.strip()
            fraktion = cols[4].text.strip()
            #email = cols[5].find('a')['href'].replace('mailto:', '').strip()  # Optional: E-Mail extrahieren
            if fraktion != 'AfD':
                mdl_info_list.append(
                    {'Nachname': nachname, 'Vorname': vorname, 'Titel': titel, 'Fraktion': fraktion}
                )

    # Browser schließen
    driver.quit()

    return mdl_info_list

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
