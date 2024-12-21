import requests
from bs4 import BeautifulSoup

base_url = "https://menuegypt.com/page/"
page_number = 1
restaurants = []

while True:
    # Generate the URL for the current page
    url = f"{base_url}{page_number}/"
    
    # Send a GET request to fetch the page content
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all restaurant cards (adjust the class based on actual inspection)
        page_restaurants = []
        for restaurant_card in soup.find_all('div', class_='restaurant-card'):  # Replace with correct class
            name = restaurant_card.find('h3', class_='restaurant-name').get_text(strip=True) if restaurant_card.find('h3', class_='restaurant-name') else 'N/A'
            location = restaurant_card.find('p', class_='restaurant-location').get_text(strip=True) if restaurant_card.find('p', class_='restaurant-location') else 'N/A'
            
            page_restaurants.append({'Name': name, 'Location': location})
        
        if page_restaurants:
            restaurants.extend(page_restaurants)  # Add the found restaurants to the list
            page_number += 1  # Go to the next page
        else:
            print("No more restaurants found or reached the last page.")
            break
    else:
        print(f"Failed to retrieve page {page_number}.")
        break

# Print the results
for restaurant in restaurants:
    print(f"Restaurant Name: {restaurant['Name']}")
    print(f"Location: {restaurant['Location']}")
    print("-" * 40)
