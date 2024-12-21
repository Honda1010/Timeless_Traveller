import requests

def fetch_hotels_in_city(city_id, api_key, currency, rooms, adults, checkin, checkout):
    """
    Fetch hotel data for a specific city using its city ID.

    Parameters:
        city_id (str): The city ID (e.g., '361058' for Cairo).
        api_key (str): API key for the MakCorps API.
        currency (str): Currency for prices (e.g., 'EGP').
        rooms (int): Number of rooms.
        adults (int): Number of adults.
        checkin (str): Check-in date (YYYY-MM-DD).
        checkout (str): Check-out date (YYYY-MM-DD).

    Returns:
        list or dict: JSON response containing hotel data or an error message.
    """
    url = "https://api.makcorps.com/city"
    params = {
        'cityid': city_id,
        'pagination': '0',
        'cur': currency,
        'rooms': rooms,
        'adults': adults,
        'checkin': checkin,
        'checkout': checkout,
        'api_key': api_key
    }

    try:
        print(f"Making request to {url} with params {params}")
        response = requests.get(url, params=params)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Replace with your actual API key.
    api_key = "6765b93f21ccbf3efa82b37c"
    city_id = "361058"  # Cairo's city ID (confirm this ID with the API documentation).
    currency = "EGP"
    rooms = 1
    adults = 2
    checkin = "2024-01-02"
    checkout = "2024-12-30"

    print("Fetching hotel data for Cairo...")
    hotel_data = fetch_hotels_in_city(city_id, api_key, currency, rooms, adults, checkin, checkout)

    print("Raw API Response:")
    print(hotel_data)
