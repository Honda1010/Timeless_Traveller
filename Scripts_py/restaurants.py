from flask import Flask
from geopy.geocoders import Nominatim
import requests
from transliterate import translit
from lang_trans.arabic import buckwalter
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
rest = Flask(__name__)
rest.secret_key = "eldosh"  # Replace with your own secret key

rest.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/tl_traveller' # username: root, password: blank, database_name: hms
db=SQLAlchemy(rest) #creating object(Database) of class SQLALCHEMY
##

governorates_info = {
    "Cairo": {"coordinates": (30.0330, 31.2330), "City_ID": 361058},
    "Alexandria": {"coordinates": (31.2156, 29.9553), "City_ID": 3610582},
    "Giza": {"coordinates": (30.0080, 31.2100), "City_ID": 361059},
    "Sharm El Sheikh": {"coordinates": (27.8800, 34.3311), "City_ID": 360545},
    "Hurghada": {"coordinates": (27.2574, 33.8116), "City_ID": 360478},
    "Luxor": {"coordinates": (25.6872, 32.6396), "City_ID": 360502},
    "Aswan": {"coordinates": (24.0889, 32.8997), "City_ID": 360542},
    "Port Said": {"coordinates": (31.2561, 32.0736), "City_ID": 360628},
    "Ismailia": {"coordinates": (30.5892, 32.2641), "City_ID": 360577},
    "Tanta": {"coordinates": (30.7867, 31.2000), "City_ID": 361110},
    "Mansoura": {"coordinates": (31.0373, 31.2366), "City_ID": 360665},
    "Zagazig": {"coordinates": (30.5890, 31.5000), "City_ID": 361287},
    "Damietta": {"coordinates": (31.4167, 31.8667), "City_ID": 360635},
    "Suez": {"coordinates": (29.9736, 32.5265), "City_ID": 360658}
}

categories={"Restaurants"}#,            "Hotels"}


class Restaurants(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    name = db.Column(db.String(100), nullable=True)  # Hotel Name
    location = db.Column(db.String(255), nullable=True)  # Hotel Location
    city_id = db.Column(db.Integer, db.ForeignKey('cities_data.city_id'), nullable=False)  # Foreign Key column

    # Relationships:
    fk_city = db.relationship('Cities_data', backref='Restaurants')

    def get_id(self):
        return str(self.id)

class Cities_data(db.Model):
    __tablename__ = 'cities_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def get_id(self):
        return str(self.id)

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


categories = {"Restaurants"}  # Categories to fetch

def get_user_location():
    """Get the user's current location (latitude and longitude)."""
    geolocator = Nominatim(user_agent="MyGeoApp")
    location = geolocator.geocode("Cairo, Egypt")  # Replace with real address for testing
    if location:
        return location.latitude, location.longitude
    else:
        raise Exception("Unable to retrieve location. Check your geolocator settings.")

def get_nearby_places(cat, lat, lon, radius=100000, api_key="fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="):
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
        "query": f"{cat}",     # Search for places
        "limit": 10,           # Number of results to return
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

    with rest.app_context():  # Create an application context
        # Iterate through the governorates and fetch places
        for cat in categories:


            for governorate, info in governorates_info.items():
                city_id = info["City_ID"]
                lat, lon = info["coordinates"]
                print(f"Fetching {cat} near {governorate} (Lat: {lat}, Lon: {lon})...")

                new_city = Cities_data(
                        city_id=city_id,
                        city_name=governorate,
                        longitude=lon,
                        latitude=lat
                    )
                db.session.add(new_city)
                db.session.commit()

                # Get nearby places
                places = get_nearby_places(cat, lat, lon, api_key=api_key)

                if places:
                    print(f"\nNearby {cat}s in {governorate} with ID:{city_id}:")
                    for place in places:
                        name = place.get("name", "Unknown Place")
                        address = place.get("location", {}).get("formatted_address", "Address not available")

                        name = enhanced_transliteration(name)
                        print(f"{cat} Name: {name}, Address: {address}")
                        
                        if cat == "Restaurants":
                            new_place = Restaurants(
                                name=name,
                                location=address,
                                city_id=city_id
                            )
                            db.session.add(new_place)
                            db.session.commit()
                else:
                    print(f"No places found in {governorate}.")
                print("-" * 50)  # Separator for clarity

if __name__ == "__main__":
    main()
