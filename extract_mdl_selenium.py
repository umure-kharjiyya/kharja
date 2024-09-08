from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Starte den Webdriver (angenommen, du nutzt Chrome)
driver = webdriver.Chrome()

# Öffne die Webseite
driver.get('https://www.bayern.landtag.de/abgeordnete/abgeordnete-von-a-z/')

# Warte, bis das Dropdown-Element sichtbar und interagierbar ist
wait = WebDriverWait(driver, 10)  # 10 Sekunden warten, bis das Element geladen ist
dropdown_element = wait.until(EC.presence_of_element_located((By.NAME, 'tx_stbltabgeordnete_filter[perpage]')))

# Finde das Dropdown-Element anhand seines Namens
dropdown = Select(dropdown_element)

# Setze den Wert auf "alle"
dropdown.select_by_value('0')  # '0' scheint der Wert für "alle" zu sein

# Überprüfe den ausgewählten Wert
# Nach der Auswahl des Wertes muss eventuell das Element erneut gefunden werden
dropdown_element = wait.until(EC.presence_of_element_located((By.NAME, 'tx_stbltabgeordnete_filter[perpage]')))
dropdown = Select(dropdown_element)
selected_option = dropdown.first_selected_option
print(f"Ausgewählter Wert: {selected_option.text}")

# Schließe den Browser
#driver.quit()


