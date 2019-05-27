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
1. Starting at a predefined url containing information for country. 
   - State information harcoded to [this](https://en.wikipedia.org/wiki/U.S._state) in the code.
      - The page is scraped to land into the pages of individual states on Wiki, which leads us to the respective cities in the state.
   - City List Page harcoded to  [this](https://en.wikipedia.org/wiki/Category:Lists_of_cities_in_the_United_States_by_state) in the code.
      - The page is scraped to add any city not found via above link.
   - State University List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_state_universities_in_the_United_States) in the code.
      - The page is scraped to find if a city has a state university. Any additional city discovered is also added to city list.
   - Airport List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States) in the code.
      - The page is scraped to map city to airport. Any additional city discovered is also added to city list.
   - Port List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_ports_in_the_United_States) in the code.
      - The page is scraped to map city to port. Any additional city discovered is also added to city list.
2. The individual state page are then scraped to find the lists or url's of cities present in it
   - Direct URL for city is obtained
   - URL to page containing list of city is obtained. Form here the URL to individual city pages are scraped.
3. The final target URL containing the city information is scraped for extracting city data from it.
   - If the city page contains a seperate page on transportation the same is used to extract additional transportation information.

## Output File Info
- city_data.csv 
  Contains the final output data
- CityURLList.txt
  An intermediate file containing all the city URL's obtained
