from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Part 1 - Scrape the links, addresses, and prices of the rental properties

# Set headers to mimic a browser request
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Send a GET request to the webpage and parse the HTML content
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# Extract all links to individual listings
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_link_elements]

# Extract all addresses and clean them up
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]

# Extract all prices and clean them up
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]

# Print the scraped data
print(f"There are {len(all_links)} links to individual listings in total:\n")
print(all_links)
print(f"\nAfter having been cleaned up, the {len(all_addresses)} addresses now look like this:\n")
print(all_addresses)
print(f"\nAfter having been cleaned up, the {len(all_prices)} prices now look like this:\n")
print(all_prices)

# Part 2 - Fill in the Google Form using Selenium

# Define Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Path to ChromeDriver executable
chrome_driver_path = r"C:\chromedriver.exe"

# Create a WebDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# Open the Google Form link
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeNYANr2b5oI0V_roQKc_3H4DEU2xey97vfokzs0p4KaMDm2Q/viewform?usp=sf_link")

time.sleep(2)

# Fill the form
for n in range(len(all_links)):
    # Find input fields by XPath and send scraped data
    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])

# Submit the form
submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
submit_button.click()

