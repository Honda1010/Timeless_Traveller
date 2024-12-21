from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome in headless mode
options = Options()
options.headless = True  # Enable headless mode

# Set the path to your ChromeDriver executable
driver_path = "/path/to/chromedriver"  # Adjust this path

# Initialize WebDriver
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Open the TripAdvisor page
url = 'https://www.tripadvisor.com/Hotels-g294201-a_trating.50-Cairo_Cairo_Governorate-Hotels.html'
driver.get(url)

# Wait for the page to load and find the hotel name elements
try:
    # Wait until the hotel names are loaded (this may need adjustment based on actual content)
    hotels = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._1jp6a0pT'))  # CSS selector for hotel names
    )

    # Extract hotel names from the found elements
    for hotel in hotels:
        hotel_name = hotel.text
        print(hotel_name)

finally:
    # Close the browser
    driver.quit()