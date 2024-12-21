from geopy.geocoders import Nominatim
import requests
from transliterate import translit

from lang_trans.arabic import buckwalter

def enhanced_transliteration(arabic_text):
    # Transliterate using Buckwalter
    transliterated_text = buckwalter.transliterate(arabic_text)
    
    # Map for refining transliteration to make it more readable
    refinement_map = {
        'A': 'a',  # Convert 'A' to 'a' for natural English-like sound
        'S': 's', 'D': 'd', 'T': 't', 'Z': 'z',  # Adjust emphatic letters
        'p': 'h',  # Convert 'p' to 'h' for the Arabic "ة"
    }
    
    # Refine Buckwalter transliteration
    readable_text = "".join(refinement_map.get(char, char) for char in transliterated_text)
    
    # Capitalize proper nouns (e.g., "Dar" instead of "dar")
    words = readable_text.split()
    refined_words = [word.capitalize() for word in words]
    
    return " ".join(refined_words)



governorates = {
    "Cairo": (30.0330, 31.2330)
    # "Cairo": (30.0330, 31.2330),
    # "Alexandria": (31.2156, 29.9553),
    # "Giza": (30.0080, 31.2100),
    # "Aswan": (24.0889, 32.8997),
    # "Luxor": (25.6872, 32.6396),
    # "Suez": (29.9736, 32.5265),
    # "Port Said": (31.2561, 32.0736),
    # "Ismailia": (30.5892, 32.2641),
    # "Tanta": (30.7867, 31.2000),
    # "Mansoura": (31.0373, 31.2366),
    # "Zagazig": (30.5890, 31.5000),
    # "Minya": (28.1000, 30.7500),
    # "Beni Suef": (29.0600, 31.1000),
    # "Assiut": (27.1800, 31.1850),
    # "Sohag": (26.5581, 31.6967),
    # "Qena": (26.1628, 32.7131),
    # "Kafr El Sheikh": (31.1167, 30.8000),
    # "Dakahlia": (31.0556, 31.9750),
    # "Beheira": (31.0900, 30.8000),
    # "Sharqia": (30.5950, 31.4440),
    # "Faiyum": (29.3100, 30.8400),
    # "Gharbia": (30.8040, 31.2460),
    # "Red Sea": (22.3569, 33.6224),
    # "New Valley": (25.7047, 28.7231),
    # "Matruh": (31.3543, 27.2596),
    # "North Sinai": (30.5851, 32.2670),
    # "South Sinai": (28.5100, 33.6067)
}

categories={"Restaurants"}#,            "Hotels"}

def get_user_location():
    """Get the user's current location (latitude and longitude)."""
    # geolocator = Nominatim(user_agent="geoapiExercises")
    geolocator = Nominatim(user_agent="MyGeoApp")

    # Test with a specific address or fallback coordinates

    location = geolocator.geocode("Cairo, Egypt")  # Replace with a real address for testing
    if location:
        return location.latitude, location.longitude
    else:
        raise Exception("Unable to retrieve location. Check your geolocator settings.")

def get_nearby_places(cat,lat, lon, radius=100000, api_key="fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="):
    """Fetch nearby places using the Foursquare Places API."""
    url = "https://api.foursquare.com/v3/places/search"
    
    headers = {
        "Accept": "application/json",
        "Authorization": api_key,
        "User-Agent": "geoapiExercises"
    }
    params = {
        "ll": f"{lat},{lon}",  # Latitude and Longitude
        "radius": radius,      # Search radius in meters
        "query": f"{cat}",  # Search for places
        "limit": 10,            # Number of results to return
        "locale": "en"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        response_json = response.json()
        if "results" in response_json:
            return response_json["results"]
        else:
            return None
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None

def main():
    api_key = "fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="  # Replace with your Foursquare API key

    # Iterate through the governorates and fetch places
    for cat in categories:
        for governorate, coords in governorates.items():
            lat, lon = coords
            print(f"Fetching {cat} near {governorate} (Lat: {lat}, Lon: {lon})...")
            
            # Get nearby places
            places = get_nearby_places(cat,lat, lon, api_key=api_key)
            
            if places:
                print(f"\nNearby {places} in {governorate}:")
                for place in places:
                    name = place.get("name", "Unknown Place")
                    address = place.get("location", {}).get("formatted_address", "Address not available")

                    # if '(' in address and ')' in address:
                    #     # Extract the restaurant name (before the parentheses)
                    #     place_name = address.split('(')[0].strip()
                    #     # Print the restaurant name and address
                    #     print(f"Restaurant Name: {place_name}, Address: {address}")
                    # else:
                    #     print(f"Restaurant Name: {name}, Address: {address}")

                    # Print the restaurant name and address
                    name=enhanced_transliteration(name)
                    print(f"{cat} Name: {name}, Address: {address}")

            else:
                print(f"No places found in {governorate}.")
            print("-" * 50)  # Separator for clarity

if __name__ == "__main__":
    main()
    
# curl -X GET "https://api.foursquare.com/v3/places/search?ll=40.748817,-73.985428&radius=1000" 
# -H "Accept: application/json" 
# -H "Authorization: fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="

# from googletrans import Translator

# def transliterate_arabic(arabic_text):
#     translator = Translator()
#     result = translator.translate(arabic_text, src='ar', dest='en')
#     return result.pronunciation or result.text  # Fallback to text if pronunciation unavailable

# # Test it
# arabic_text = "دار الكتب المصرية"
# print(transliterate_arabic(arabic_text))
