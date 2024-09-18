import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def extract_mdl_info():
    base_url = 'https://www.thueringer-landtag.de'
    url = f'{base_url}/abgeordnete/abgeordnete-fraktionen-gruppe-sitzordnung/#tab-2'

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    mdl_info_list = []

    # Find the list of url links
    links = soup.find_all('div', class_='teaser-box')
    seen_members = []

    for link in links:
        # Extract the detail page link (usually in an 'a' tag around the image or name)
        link_tag = link.find('a', class_='more icon-arrow', href=True)
        if link_tag:
            detail_url = base_url + link_tag['href']

            # Now scrape the member detail page
            detail_response = requests.get(detail_url)
            if detail_response.status_code != 200:
                print(f"Fehler beim Abrufen der Detailseite: {detail_response.status_code}")
                continue

            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            # Extract the name and faction from the detail page
            name_tag = detail_soup.find('title')  # Adjust the class based on the actual HTML structure
            fraktion_tag = detail_soup.find('strong')  # Adjust the class

            a_tags = detail_soup.find_all('a')
            email = None
            for tag in a_tags:
                href =tag.get('href', '')
                if href.startswith('mailto:'):
                    email = href[len('mailto:'):].strip()

            if name_tag and fraktion_tag:
                full_name = name_tag.get_text(strip=True)
                if full_name in seen_members:
                    continue
                seen_members.append(full_name)
                fraktion = fraktion_tag.get_text(strip=True).split(',')[0].strip()
                # Split full name into first name (Vorname) and last name (Nachname)
                names_parts = full_name.split(' ')
                if len(names_parts) >= 2:
                    vorname = ' '.join(names_parts[:-1]).strip()
                    nachname = names_parts[-1].strip()
                else:
                    vorname = names_parts[0].strip()
                    nachname = ""

                # Skip AfD members
                if 'AfD' not in fraktion:
                    mdl_info_list.append({
                        'Nachname': nachname,
                        'Vorname': vorname,
                        'Fraktion': fraktion,
                        'Email': email
                    })

            # Adding a short delay between requests to avoid overwhelming the server
            # time.sleep(1)

    return mdl_info_list


def save_to_excel(data, file_name='mdl_info_thueringen.xlsx'):
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    if mdl_info_list:
        # save_to_excel(mdl_info_list)
        print(f"{len(mdl_info_list)} Einträge gefunden.")
    else:
        print("Keine Einträge gefunden.")
