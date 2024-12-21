import requests
from bs4 import BeautifulSoup


# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Agricultural_Museum,_Egypt"

# Send a GET request to the page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

wikipedia_museum_links = [
    "Egyptian_Museum",
    "Egyptian_National_Military_Museum",
    "Child_Museum_(Cairo)",
    "Coptic_Museum",
    "Aswan_Museum",
    "Alexandria_National_Museum",
    "Abdeen_Palace",
    "Bibliotheca_Alexandrina",
    "Imhotep_Museum",
    "Graeco-Roman_Museum",
    "Manial_Palace_and_Museum",
    "Mukhtar_Museum"
    "Mummification_Museum"
    "Grand_Egyptian_Museum"
]

# Extracting the required information
def extract_info():
    # Page title as the name
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

    # Location and type from the infobox
    infobox = soup.find("table", {"class": "infobox"})
    rows = infobox.find_all("tr") if infobox else []

    location, type_ = None, None

    for row in rows:
        header = row.find("th")
        data = row.find("td")

        if header and data:
            header_text = header.text.strip().lower()

            # Check for location-related headers
            if "location" in header_text or "city" in header_text or "town" in header_text:
                location = data.text.strip()
            # Check for type-related headers
            elif "type" in header_text or "architecture" in header_text or "architect" in header_text:
                type_ = data.text.strip()

    return {
        "Name": name,
        "Location": location,
        "Type": type_,
    }

# Get the extracted data
info = extract_info()

# Print the result
for key, value in info.items():
    print(f"{key}: {value}")


# def update_museums():
#     for museum_link in wikipedia_museum_links:
#         info = extract_info_museum(museum_link)
#         current_museum = Museums(
#             Name = info['Name'],
#             Location = info['Location'],
#             Type = info['Type']
#         )
#         db.session.add(current_museum)
#         db.session.commit()