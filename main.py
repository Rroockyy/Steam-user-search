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
    
    return soup

# Usage

print("Enter username to search: ")
username = input()
print("Enter real name to search (optional): ")
realName = input()
print("Enter location to search (optional): ")
location = input()
print("Does the person have a profile picture? y/n (optional): ")
pfpPresent = input()

page = 1
steamURL = "https://steamcommunity.com/search/users/#page=" + str(page) + "&text=" + username
css_selector = ".search_row"
soup = wait_and_scrape(steamURL, css_selector)
mydivs = soup.find_all("div", {"class": "search_row"})
for user in mydivs:
    userSiblings = []
    for element in user.find("a", {"class": "searchPersonaName"}).next_siblings:
        userSiblings.append(element)

    currentUsername = user.find("a", {"class": "searchPersonaName"}).text

    currentRealName = userSiblings[1].strip()
    if len(userSiblings) == 4 and userSiblings[-1] == ' ':
        currentRealName = ""

    currentLocation = ""
    if userSiblings[-1] == ' ':
        currentLocation = userSiblings[-3].strip()

    currentHasPfp = True
    if user.find("img")['src'] == "https://avatars.fastly.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_medium.jpg":
        currentHasPfp = False

    profileURL = user.find("a")['href']
        
    print(currentUsername)
    print(currentRealName)
    print(currentLocation)
    print(currentHasPfp)
    print(profileURL)
    print()