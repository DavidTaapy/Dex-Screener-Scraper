# Dex Screener Project

## Project Description

The following project was built to scrape https://dexscreener.com/new-pairs using the Selenium package as the website is dynamically loaded. This allows us to retrieve the latest financial data regarding cryptocurrency pairs that can be used for trading / trend analysis!

## Required Technologies

The following technologies are required for the program to work:

- Web Driver (I chose to use Firefox Web Driver)

## Project Methods

The sample output csv that will be produced after scraping Dex Screener can be found as 'Data.csv'! The data are filtered, by removing those with less than $2 Million Market Cap as well as those with ridiculous Market Caps, before the various pairs are sorted in descending order by Market Cap!

## Project Requiremenets

As the number of pages on Dex Screener may vary due to the market, the program must dynamically go to the next page until there are no new pages to retrieve all the relevant data as manual url provision might lead to errors and be troublesome!

## Update

Due to website starting to introduce anti-bot mechanics such as Cloudflare, it has hindered the bot's ability to scrape data from the website for analysis! Therefore, the bot was changed to be equipped with the ability to overcome these obstacles!