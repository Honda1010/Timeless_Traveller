import requests
from bs4 import BeautifulSoup

def extract_attraction():
    
    url = "https://en.wikipedia.org/wiki/Temple_of_Edfu"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

    # Attributes to extract
    attributes = {
        "Location": None,
        "Type": None,
        "Built": None,
        "Part of": None,
        "Builders": None,
        "Periods": None,
    }

    # Locate the infobox
    infobox = soup.find("table", {"class": "infobox"})
    rows = infobox.find_all("tr") if infobox else []

    # Loop through rows to find attributes
    for row in rows:
        header = row.find("th")
        data = row.find("td")

        if header and data:
            header_text = header.text.strip().lower()

            if "location" in header_text:
                attributes["Location"] = data.text.strip()
            elif "type" in header_text:
                attributes["Type"] = data.text.strip()
            elif "built" in header_text or "founded" in header_text or "constructed" in header_text:
                attributes["Built"] = data.text.strip()
            elif "part of" in header_text:
                attributes["Part of"] = data.text.strip()
            elif "builder" in header_text:
                attributes["Builders"] = data.text.strip()
            elif "period" in header_text:
                attributes["Periods"] = data.text.strip()

    # Add the name to the attributes
    attributes["Name"] = name
    return attributes

# Get the extracted data
info = extract_attraction()

# Print the result
for key, value in info.items():
    print(f"{key}: {value}")
