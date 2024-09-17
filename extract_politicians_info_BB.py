import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_mdl_info():
    url = 'https://www.landtag.brandenburg.de/de/abgeordnete_-_fraktionen/abgeordnete/abgeordnete_im_ueberblick/25777'  # Placeholder for the actual page URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    mdl_info_list = []

    # Find the list of sections containing member data
    sections = soup.find_all('section', id=True)

    for section in sections:
        # Find all 'a' tags with class 'jumplist-item' inside the section
        items = section.find_all('a', class_='jumplist-item')
        for item in items:
            # Extract the name from the 'h6' tag within the 'figcaption'
            name_tag = item.find('h6')
            # Extract the faction from the 'span' tag within the 'figcaption'
            fraktion_tag = item.find('span')
            if name_tag and fraktion_tag:
                full_name = name_tag.get_text(strip=True)
                fraktion = fraktion_tag.get_text(strip=True)

                # Split name into 'Vorname' and 'Nachname' (assuming a single name)
                names_parts = full_name.split(' ')
                if len(names_parts) >= 2:
                    nachname = names_parts[-1].strip()
                    vorname = ' '.join(names_parts[:-1]).strip()
                else:
                    vorname = names_parts[0].strip()
                    nachname = ""

                # Text 'Fraktion' entfernen
                if '-Fraktion' in fraktion:
                    fraktion =fraktion.split('-')[0]
                elif ' Fraktion' in fraktion:
                    fraktion =fraktion.split(' ')[0]
                elif 'Fraktion ' in fraktion:
                    fraktion = fraktion.split(' ')[1:]
                    fraktion =' '.join(fraktion)
                # Append the information to the list
                if 'AfD' not in fraktion:
                    mdl_info_list.append({
                    'Name': nachname,
                    'Vorname': vorname,
                    'Fraktion': fraktion
                })

    return mdl_info_list

def save_to_excel(data, file_name='mdl_info_brandenburg.xlsx'):
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    # Uncomment the next line to save to an Excel file
    # save_to_excel(mdl_info_list)
    print(f"{len(mdl_info_list)} Einträge gefunden.")
    for mdl_info in mdl_info_list:
        print(mdl_info)
