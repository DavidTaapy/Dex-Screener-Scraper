# Importing libraries
from numpy import NaN, True_
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from seleniumbase import Driver

# Function to turn retrieved data into a dataframe
def processData(data, firstIndex):
    # Remove V2 Column
    data = list(filter(lambda x: x not in ['V1', 'V2', 'V3'], data))
    # Change here if first column is changed
    firstColumn = "TOKEN"   
    firstColumnIndex = data.index(firstColumn)
    # First Data Element
    indexString = "#" + str(firstIndex)
    if indexString in data:
        firstDataIndex = data.index(indexString)
    else:
        return "Error in getting first data index!"
    # Get number of columns by deducted index of first data element from index of first column element   
    numColumns = firstDataIndex - firstColumnIndex + 2 # The two additional ones are the "#Num" & "Token Pair"
    numColumnsPreMerge = numColumns + 2 # Token-Currency Pair Currently Split Into 3 Parts - 'Token' '/' 'Currency'
    # Get the column names
    columns = ["Number", "Currency Pair"]
    columns += data[firstColumnIndex : firstColumnIndex + numColumns - 2] # Minus 2 as we already have the first two columns in the columns list
    # Initialise new dataframe
    df = pd.DataFrame(columns = columns)
    df_length = 0
    # Add the data into the dataframe
    while firstDataIndex < len(data):
        to_reduce_2 = False
        to_reduce_1 = False
        # Get data for given row
        rowElements = data[firstDataIndex : firstDataIndex + numColumnsPreMerge]
        # Handle foreign names that are hidden
        # if not rowElements[1].isascii():
        #     rowElements.insert(4, rowElements[1])
        #     rowElements = rowElements[:-1]
        #     firstDataIndex -= 1
        # Replace the currency sign
        for element in rowElements:
            if ('$' in element and '.' in element) or element == '$0':  # Find Price
                priceIndex = rowElements.index(element)
                break
        # Merge the currency, slash and token as mentioned above
        if priceIndex != 2:
            rowElements[1] += rowElements[2] + rowElements[3]
            if priceIndex == 4:
                rowElements.insert(4, rowElements[3])
                to_reduce_1 = True
            del rowElements[2]
            del rowElements[3]
        else:
            to_reduce_2 = True
        # Get the final row elements
        finalRowElements = rowElements[0 : priceIndex]
        # Some names are not retrieved properly from DexScreener - Replace with NIL
        tempNumColumns = numColumns
        while len(finalRowElements) < 3:
            finalRowElements.append("NIL")
            tempNumColumns -= 1
            firstDataIndex -= 1
        finalRowElements += rowElements[priceIndex : tempNumColumns]
        # print(finalRowElements)
        df.loc[df_length] = finalRowElements # Add data elements as a row to dataframe
        firstDataIndex += numColumnsPreMerge # Increment index to become the first element of the next data row
        if to_reduce_2:
            firstDataIndex -= 2
        elif to_reduce_1:
            firstDataIndex -= 1
        df_length += 1 # Increment number of rows in dataframe
    
    return df

# Process Data After Retrieval
def postProcess(df):
    # Dictionary for units
    units = {
        'M': 10 ** 6,
        'B': 10 ** 9,
        'T': 10 ** 12
    }

    # Remove tokens with absurd Market Capitalisation
    df = df.loc[df['FDV'] != '>$999T']
    # Keep tokens with units Millions, Billions, Trillions
    df = df.loc[df['FDV'].str.contains("[M,B,T]$")]
    # Convert Market Cap to Integer
    df['FDV'] = df['FDV'].apply(lambda x: float(x[1: -1]) * (units[x[-1]]))
    # Remove entries with Market Cap less than 2 Million
    twoMillion = 2 * (10 ** 6)
    df = df.loc[df['FDV'] >= twoMillion]
    # Sort Market Cap in descending order
    df = df.sort_values(by = ['FDV'], ascending = False)

    return df

# Scrape Dex Screener For Data
def scrapeDex():
    startTime = time.time()  # Time the program was started
    # Initialize the URLs - Add the first pages of the genre to scrape
    urls = [   
        "https://dexscreener.com/new-pairs"             # First Page of New Pairs
    ]        
    
    # Initialize Driver
    # driver = uc.Chrome()
    driver = Driver(uc=True)
    
    while True:
    # Scrape each url page
        for url in urls:
            # Initialize Empty Dataframe
            masterDf = pd.DataFrame()
            # Set first index of current page
            firstIndex = 1       
            while True:
                # Statement to inform about progress
                print('Scraping with first index = {0}'.format(firstIndex))
                try:
                    driver.get(url)
                    data = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ds-dex-table'))
                    )
                    nextData = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'custom-v0p5eh'))
                    )
                    if data:
                        data = data.text.split('\n')
                        tempDf = processData(data, firstIndex)
                        masterDf = masterDf.append(tempDf)
                        firstIndex += 100
                        if str(firstIndex) not in nextData.text:
                            break
                        else:
                            # Change url to include new page number
                            if "page" not in url:   # If first page
                                url += "/page-2"
                            else:
                                baseURL, pageNum = url.split("page-")   # If a page number is already present
                                url = baseURL + "page-" + str(int(pageNum) + 1)
                    time.sleep(1) # Delay by one second
                except Exception as e:
                    print(e)
                    continue
            # Post Process Dataframe
            masterDf = postProcess(masterDf)
            # Export the table
            masterDf.to_csv("Data.csv", index = False)
        # Sleep for remaining time left in three minutes
        time.sleep(180.0 - (time.time() - startTime) % 180.0)

# Run the following when program is executed
if __name__ == "__main__":
    scrapeDex()