# Importing libraries
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the URLs
urls = [
    "https://dexscreener.com/new-pairs",                # First Page of New Pairs 
    "https://dexscreener.com/new-pairs/page-2",         # Second Page of New Pairs
    "https://dexscreener.com/new-pairs/page-3",         # Third Page of New Pairs
    "https://dexscreener.com/new-pairs/page-4"          # Fourth Page of New Pairs
]

# Function to turn retrieved data into a dataframe
def processData(data):
    # Remove V2 Column
    data = list(filter(lambda x: x != 'V2', data))
    # Change here if first column is changed
    firstColumn = "TOKEN"   
    firstColumnIndex = data.index(firstColumn)
    # First Data Element
    if data.index("#1"):
        firstDataIndex = data.index("#1")
    elif data.index("#101"):
        firstDataIndex = data.index("#101")
    elif data.index("#201"):
        firstDataIndex = data.index("#201")
    elif data.index("#301"):
        firstDataIndex = data.index("#301")
    else:
        return "Error in getting first data index!"
    # Get number of columns by deducted index of first data element from index of first column element   
    numColumns = firstDataIndex - firstColumnIndex + 2 # The two additional ones are the "#Num" & "Token Pair"
    # Find the number of rows
    numRows = int((len(data) - firstDataIndex) / numColumns)
    # Get the column names
    columns = ["Number", "Currency Pair"]
    columns += data[firstColumnIndex : firstColumnIndex + numColumns - 2] # Minus 2 as we already have the first two columns in the columns list
    # Initialise new dataframe
    df = pd.DataFrame(columns = columns)
    df_length = 0
    # Add the data into the dataframe
    for _ in range(numRows):
        rowElements = data[firstDataIndex : firstDataIndex + numColumns]
        df.loc[df_length] = rowElements # Add data elements as a row to dataframe
        firstDataIndex += numColumns # Increment index to become the first element of the next data row
        df_length += 1 # Increment number of rows in dataframe
    
    return df

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
            data = data.text.split('\n')
            tempDf = processData(data)
            print(tempDf)
        break
        time.sleep(1) # Delay by one second
    except Exception as e:
        print(e)
        continue
# Close Driver
driver.close()

# Combine the tables
# results = pd.concat(tables, axis = 0)
# results.to_excel('Dex Screener.xlsx', index = False)