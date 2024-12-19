import requests
import mysql.connector
from mysql.connector import Error
import time
# Foursquare API Configuration
API_KEY = "fsq3LdgY4ZF2fysqBSvAkILuTss4gok010MDzlPNG4soZd4="
BASE_URL = "https://api.foursquare.com/v3/places/search"
HEADERS = {
    "Authorization": API_KEY
}

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tl_traveller"
}

# Categories for fetching data
CATEGORIES = {
    "historical_places": "16056",   # Historical places
    "restaurants": "13065",        # Restaurants
    "hotels": "19014",             # Hotels
    "entertainment": "10032"       # Entertainment
}

#Test the Connection
# try:
#     connection = mysql.connector.connect(**DB_CONFIG)
#     if connection.is_connected():
#         print("Connected to MySQL database!")
# except mysql.connector.Error as e:
#     print(f"Database error: {e}")
# finally:
#     if connection.is_connected():
#         connection.close()


# Fetch places from Foursquare API with pagination
def fetch_places(lat, lon, radius=50000, category="", limit=50):
    """Fetch places from Foursquare API with pagination."""
    params = {
        "ll": f"{lat},{lon}",
        "radius": radius,
        "categories": category,
        "limit": limit
    }
    all_places = []

    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            all_places.extend(data.get("results", []))
            
            # Check if there's a next page (pagination)
            next_page = data.get("next_page", None)
            if not next_page:
                break
            else:
                params['next_page'] = next_page
            
            # Delay to prevent rate-limiting
            time.sleep(1)
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

    return all_places

# Save places to MySQL database
def save_places_to_db(places):
    """Save places to the database with duplicate checks."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Create the Places table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS All_Places (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                address TEXT,
                latitude FLOAT,
                longitude FLOAT,
                category VARCHAR(255),
                UNIQUE(name, latitude, longitude)  -- Prevent duplicates
            )
        """)

        # Insert places into the table, ignoring duplicates
        for place in places:
            name = place.get("name", "Unknown")
            location = place.get("location", {})
            address = location.get("formatted_address", "Address not available")
            latitude = location.get("lat", 0.0)
            longitude = location.get("lng", 0.0)
            categories = place.get("categories", [])
            category = ", ".join([cat.get("name", "Uncategorized") for cat in categories]) if categories else "Uncategorized"

            cursor.execute("""
                INSERT IGNORE INTO All_Places (name, address, latitude, longitude, category)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, address, latitude, longitude, category))

        connection.commit()
        print(f"{cursor.rowcount} places saved to the database.")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main execution
def main():
    # Coordinates for Egypt's approximate center
    lat, lon = 26.8206, 30.8025
    radius = 1000000  # 50 km

    all_places = []

    # Fetch data for each category
    for category_name, category_id in CATEGORIES.items():
        print(f"Fetching data for category: {category_name}")
        places = fetch_places(lat, lon, radius, category_id)
        all_places.extend(places)

    # Save all fetched places to the database
    save_places_to_db(all_places)

if __name__ == "__main__":
    main()

