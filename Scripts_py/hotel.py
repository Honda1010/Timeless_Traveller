import requests
from bs4 import BeautifulSoup

wikipedia_links = [
    "Cecil_Hotel_(Alexandria)",
    "El_Safa_Palace",
    "Cairo_Marriott_Hotel",
    "Fairmont_Nile_City",
    "Grand_Nile_Tower_Hotel",
    "Mena_House_Hotel",
    "Semiramis_InterContinental_Hotel",
    "Sofitel_Cairo_Nile_El_Gezirah_Hotel",
    "Windsor_Hotel_(Cairo)",
    "Steigenberger_Hotel_%26_Nelson_Village",
    "Old_Cataract_Hotel"
]


def extract_info_hotel(h_name):
    data = h_name
    url = f"https://en.wikipedia.org/wiki/{data}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

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

# def update_hotels():
#     for hotel_link in wikipedia_links:
#         info = extract_info_hotel(hotel_link)
#         current_hotel = Hotels(
#             Name = info['Name'],
#             Location = info['Location'],
#             Opening = info['Opening'],
#             Owner = info['Owner'],
#             Rooms = info['Number of Rooms']
#         )
#         db.session.add(current_hotel)
#         db.session.commit()