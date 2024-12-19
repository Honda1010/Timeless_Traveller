# from geopy.geocoders import Nominatim
# import requests
# from transliterate import translit

# def get_user_location():
#     """Get the user's current location (latitude and longitude)."""
#     # geolocator = Nominatim(user_agent="geoapiExercises")
#     geolocator = Nominatim(user_agent="MyGeoApp")

#     # Test with a specific address or fallback coordinates

#     location = geolocator.geocode("Cairo, Egypt")  # Replace with a real address for testing
#     if location:
#         return location.latitude, location.longitude
#     else:
#         raise Exception("Unable to retrieve location. Check your geolocator settings.")

# def get_nearby_historical_places(lat, lon, radius=100000, api_key="fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="):
#     """Fetch nearby historical places using the Foursquare Places API."""
#     url = "https://api.foursquare.com/v3/places/search"
#     # url="https://api.foursquare.com/v3/places/search?ll=40.748817,-73.985428&radius=1000" 

#     headers = {
#         "Accept": "application/json",
#         "Authorization": "fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4=",  # Make sure this API key is correct and has necessary permissions
#         "User-Agent": "geoapiExercises" 
#     }
#     params = {
#         "ll": f"{lat},{lon}",  # Latitude and Longitude
#         "radius": radius,      # Search radius in meters
#         "query": "museum",  # Search for historical places
#         "limit": 10,            # Number of results to return
#         "locale": "en"
#     }
    
#     response = requests.get(url, headers=headers, params=params)
#     # response = requests.get(url, headers=headers)
    
#     # Debugging: Print the raw response to inspect the data
#     print(f"Response Status Code: {response.status_code}")
#     print(f"Response Text: {response.text}")

#     if response.status_code == 200:
#         response_json = response.json()
#         if "results" in response_json:
#             return response_json["results"]
#         else:
#             raise Exception("No results found in the API response.")
#     else:
#         raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

# def main():

#     # latitude, longitude = get_user_location()
#     # # print(f"Your current location is: Latitude={latitude}, Longitude={longitude}")
#     # print(f"Your current location is: Latitude={latitude}, Longitude={longitude}")

#     try:
#         # Get the user's current location
#         latitude, longitude = get_user_location()
#         print(f"Your current location is: Latitude={latitude}, Longitude={longitude}")

#         # Get nearby historical places
#         api_key = "fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="  # Replace with your Foursquare API key
#         historical_places = get_nearby_historical_places(latitude, longitude, api_key=api_key)
        
#         # Display the historical places
#         if historical_places:
#             print("\nNearby Historical Places:")
#             for place in historical_places:
#                 name = place.get("name", "Unknown Place")
#                 address = place.get("location", {}).get("formatted_address", "Address not available")
#                 name_transliterated=translit(name,'ar',reversed=True)
#                 address_transliterated=translit(address,'ar',reversed=True)

#                 # try:
#                 #     name_transliterated=translit(name,'ar',reversed=True)
#                 #     address_transliterated=translit(address,'ar',reversed=True)
#                 # except Exception as e:
#                 #     name_transliterated=name
#                 #     address_transliterated=name
  
#                 print(f"- {name_transliterated} ({address_transliterated})")

#         else:
#             print("No historical places found nearby.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

# # curl -X GET "https://api.foursquare.com/v3/places/search?ll=40.748817,-73.985428&radius=1000" 
# # -H "Accept: application/json" 
# # -H "Authorization: fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="

from googletrans import Translator

def transliterate_arabic(arabic_text):
    translator = Translator()
    result = translator.translate(arabic_text, src='ar', dest='en')
    return result.pronunciation or result.text  # Fallback to text if pronunciation unavailable

# Test it
arabic_text = "دار الكتب المصرية"
print(transliterate_arabic(arabic_text))
