import requests
from bs4 import BeautifulSoup

Hotels=["Fairmont_Nile_City","Grand_Nile_Tower_Hotel","Mena_House_Hotel","Semiramis_InterContinental_Hotel"
"Shepheard%27s_Hotel","Sofitel_Cairo_Nile_El_Gezirah_Hotel","Windsor_Hotel_(Cairo)","Cairo_Marriott_Hotel"]
# URL of the Wikipedia page

data=input("please enter the hotel ")


url = f"https://en.wikipedia.org/wiki/{data}"

# Send a GET request to the page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extracting the required information
def extract_info():
    # Page title as the hotel name
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

    # Location, opening, owner, and number of rooms from the infobox
    infobox = soup.find("table", {"class": "infobox"})
    rows = infobox.find_all("tr") if infobox else []

    location, opening, owner, rooms = None, None, None, None

    for row in rows:
        header = row.find("th")
        data = row.find("td")

        if header and data:
            header_text = header.text.strip().lower()

            if "location" in header_text:
                location = data.text.strip()
            elif "opening" in header_text:
                opening = data.text.strip()
            elif "owner" in header_text:
                owner = data.text.strip()
            elif "number of rooms" in header_text:
                rooms = data.text.strip()

    return {
        "Name": name,
        "Location": location,
        "Opening": opening,
        "Owner": owner,
        "Number of Rooms": rooms,
    }

# Get the extracted data
info = extract_info()

# Print the result
for key, value in info.items():
    print(f"{key}: {value}")
