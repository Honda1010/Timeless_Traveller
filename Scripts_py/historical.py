import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_info_hotel(h_name):
    # Encode the name to handle special characters and spaces
    data = urllib.parse.quote(h_name)
    url = f"https://en.wikipedia.org/wiki/{data}"
    response = requests.get(url)

    # Check if the page was successfully fetched
    if response.status_code != 200:
        return {"Error": f"Failed to fetch the page. HTTP Status Code: {response.status_code}"}

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the name from the page title
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

    # Extract the infobox information
    infobox = soup.find("table", {"class": "infobox"})
    rows = infobox.find_all("tr") if infobox else []

    location, opening, owner, rooms, description = None, None, None, None, None

    for row in rows:
        header = row.find("th")
        data = row.find("td")

        if header and data:
            header_text = header.text.strip().lower()

            if "location" in header_text:
                location = data.get_text(" ", strip=True)
            elif "opening" in header_text:
                opening = data.get_text(" ", strip=True)
            elif "owner" in header_text:
                owner = data.get_text(" ", strip=True)
            elif "number of rooms" in header_text:
                rooms = data.get_text(" ", strip=True)

    # Extract description: Target the first meaningful paragraph
    content_div = soup.find("div", {"class": "mw-content-ltr mw-parser-output"})
    if content_div:
        # Filter paragraphs that are not empty or metadata-like
        paragraphs = content_div.find_all("p", recursive=False)
        for paragraph in paragraphs:
            text = paragraph.get_text(" ", strip=True)
            if text and not text.startswith("Coordinates") and len(text) > 30:
                description = text
                break

    # Fall back to meta description if no valid paragraph is found
    if not description:
        meta_tag = soup.find("meta", {"name": "description"})
        if meta_tag:
            description = meta_tag.get("content", "").strip()

    return {
        "Name": name,
        "Location": location,
        "Opening": opening,
        "Owner": owner,
        "Number of Rooms": rooms,
        "Description": description,
    }

# Example usage
info = extract_info_hotel("Grand_Nile_Tower_Hotel")
for key, value in info.items():
    print(f"{key}: {value}")
