import requests
from bs4 import BeautifulSoup
import mysql.connector

conn = mysql.connector.connect(
    host='localhost', 
    user='root', 
    password='', 
    database='tl_traveller'
)
cursor = conn.cursor()

def insert_place(location, name, type_):
    cursor.execute("""
        INSERT INTO historical (location,name, type_)
        VALUES (%s, %s, %s)
    """, (location,name,type_))
    conn.commit()

def scrape_places():
    search_query = "Cairo historical places"
    base_url = "https://www.google.com/"  # Replace with an actual URL that lists places
    response = requests.get(base_url + search_query)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extract place details (update with correct tags based on the website's structure)
    for place in soup.find_all('div', class_='place-item'):
        name = place.find('h2').get_text()
        type_ = place.find('span', class_='place-type').get_text()
        location = place.find('span', class_='location').get_text()
      
        insert_place(location, name, type_)
        print(name)
        print(location)
        print(type_)

# Run the scraper
scrape_places()

# Close the connection
cursor.close()
conn.close()