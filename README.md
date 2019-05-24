# WikiCityScraper

The code written in python scrapes data from wikipedia from pages that are associated with cities. It collects a wide variety of data that includes and is not limited to 'Population', 'Government', 'Climate' etc.

## Getting Started

The 'Main.py' is the only file required to execute the project.

## Prerequisites

A python run time environment with "re", "urllib", "csv" and "BeautifulSoup" library installed.

Language: Python
Data Source: Wikipedia

## Determining Top City

The code **determines the top city using a hierarchical discovery approach**, the includes the following:
1. Starting at a predefined url containing state information for country. It has been harcoded to [this](https://en.wikipedia.org/wiki/U.S._state) in the code.
   - The page is scraped to land into the pages of individual states on Wiki.
2. The individual state page are then scraped to find the lists or url's of cities present in it
   - Direct URL for city is obtained
   - URL to page containing list of city is obtained. Form here the URL to individual city pages are scraped.
3. The final target URL containing the city information is scraped for extracting city data from it.

## Output File Info
- city_data.csv 
  Contains the final output data
- CityURLList.txt
  An intermediate file containing all the city URL's obtained
