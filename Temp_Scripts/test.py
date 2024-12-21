import requests

url = "https://api.makcorps.com/city"
params = {
    'cityid': '359787', #new york
    'pagination': '0',
    'cur': 'USD',
    'rooms': '1',
    'adults': '2',
    'checkin': '2024-12-30',
    'checkout': '2025-01-03',
    'api_key': '6765f83372c8b13ee80b00e8'
}

response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    json_data = response.json()
    
    # Print or use the parsed JSON data
    print(json_data)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}, {response.text}")