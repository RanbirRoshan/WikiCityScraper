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
   - Air Force Station List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_United_States_Air_Force_installations) in the code.
      - The page is scraped to map city to air force installations. Any additional city discovered is also added to city list.
   - Federal Prison List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_United_States_federal_prisons) in the code.
      - The page is scraped to map city to fedral prisons. Any additional city discovered is also added to city list.
   - Hospital List Page harcoded to  [this](https://en.wikipedia.org/wiki/Lists_of_hospitals_in_the_United_States) in the code.
      - The page is scraped to map city to major hospital. Any additional city discovered is also added to city list.
   - Sports Arena List Page harcoded to  [this](https://en.wikipedia.org/wiki/List_of_indoor_arenas_in_the_United_States) in the code.
      - The page is scraped to map city to sports arena. Any additional city discovered is also added to city list.
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
  
## Additional Source of data aumentation
•	[Court](https://en.wikipedia.org/wiki/List_of_United_States_district_and_territorial_courts)
•	[Marine Installation](https://en.wikipedia.org/wiki/List_of_United_States_Marine_Corps_installations)
•	[National Monuments](https://en.wikipedia.org/wiki/List_of_national_monuments_of_the_United_States)
•	[City Close To national Forest (needs more information to capture all cities)](https://en.wikipedia.org/wiki/List_of_U.S._National_Forests)
•	[Cities With Aquaria](https://en.wikipedia.org/wiki/List_of_aquaria_in_the_United_States)
•	[Cities with zoo](https://en.wikipedia.org/wiki/List_of_zoos_in_the_United_States)
•	[Cities with casino](https://en.wikipedia.org/wiki/List_of_casinos_in_the_United_States)
•	[Cities with beaches](https://en.wikipedia.org/wiki/List_of_beaches_in_the_United_States)
•	[Cities with museums](https://en.wikipedia.org/wiki/List_of_museums_in_the_United_States)
•	[Cities with amusement parks](https://en.wikipedia.org/wiki/List_of_amusement_parks_in_the_Americas#_United_States)
•	[Cities with botanical gardens and arboretums](https://en.wikipedia.org/wiki/List_of_botanical_gardens_and_arboretums_in_the_United_States)
•	[Cities with nature centers](https://en.wikipedia.org/wiki/List_of_nature_centers_in_the_United_States)
•	[Cities with ski areas and resorts](https://en.wikipedia.org/wiki/List_of_ski_areas_and_resorts_in_the_United_States)
•	[Cities with auto race tracks](https://en.wikipedia.org/wiki/List_of_auto_racing_tracks_in_the_United_States)

