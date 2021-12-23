# Importing libraries
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tables = []

# Initialize the URLs
urls = [
    "https://dexscreener.com/new-pairs",                # First Page of New Pairs 
    "https://dexscreener.com/new-pairs/page-2",         # Second Page of New Pairs
    "https://dexscreener.com/new-pairs/page-3",         # Third Page of New Pairs
    "https://dexscreener.com/new-pairs/page-4"          # Fourth Page of New Pairs
]

# Initialize Driver
driver = webdriver.Firefox()
for url in urls:
    # Statement to inform about progress
    print('Scraping {0}'.format(url))
    try:
        driver.get(url)
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-18z8t27'))
        )
        if data:
            print(data.text.split('\n'))
        time.sleep(1) # Delay by one second
    except Exception as e:
        print(e)
        continue
# Close Driver
driver.close()

# Combine the tables
# results = pd.concat(tables, axis = 0)
# results.to_excel('Dex Screener.xlsx', index = False)