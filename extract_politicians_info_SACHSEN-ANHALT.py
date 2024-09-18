import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_mdl_info():
    url = 'https://www.landtag.sachsen-anhalt.de/landtag/abgeordnete/abgeordnetensuche'  # Placeholder for the actual page URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    mdl_info_list = []

    # Find the list of members
    member_list = soup.find_all('div',class_= 'wrapper')

    for member in member_list:
        # Extract the name from the 'a' tag
        name_tag = member.find('span', class_='as-h2')
        if name_tag:
            full_name = name_tag.get_text(strip=True)
            # Split the name into 'Vorname' and 'Nachname'
            names_parts = full_name.split(' ')
            if len(names_parts) >= 2:
                vorname = ' '.join(names_parts[:-1]).strip()
                nachname = names_parts[-1].strip()
            else:
                vorname = names_parts[0].strip()
                nachname = ""

            # Extract the faction from the 'span' tag
            fraktion_tag = member.find('p')
            fraktion = fraktion_tag.get_text(strip=True).split('-')[0].strip() if fraktion_tag else "Unbekannt"

            # Skip AfD entries
            if 'AfD' not in fraktion and fraktion != 'Unbekannt':
                mdl_info_list.append({
                    'Name': nachname,
                    'Vorname': vorname,
                    'Fraktion': fraktion
                })

    return mdl_info_list

def save_to_excel(data, file_name='mdl_info_sachsen-anhalt.xlsx'):
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    # save_to_excel(mdl_info_list)
    print(f"{len(mdl_info_list)} Einträge gefunden.")
    for mdl_info in mdl_info_list:
        print(mdl_info)

