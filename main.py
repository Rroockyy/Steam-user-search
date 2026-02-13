import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (optional)

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

def wait_and_scrape(url, css_selector):
    driver.get(url)
    
    # Wait for the element to be present
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )
    
    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Now you can use BeautifulSoup methods to extract data
    # For example:
    # data = soup.select(css_selector)
    
    return soup

# Usage
username = "majkel"
steamURL = "https://steamcommunity.com/search/users/#page=1&text=" + username
css_selector = ".search_row"
soup = wait_and_scrape(steamURL, css_selector)
mydivs = soup.find_all("div", {"class": "search_row"})
for user in mydivs:
    print(user.find("a", {"class": "searchPersonaName"}).text)