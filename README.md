# Web Scraping Smartphone Data from Flipkart
## Overview
This Python script is designed to scrape smartphone data from the Flipkart website, focusing on products within the price range of Rs. 10,000 to Rs. 30,000 which are assured by Flipkart excluding out-of-stock. The script extracts key information such as smartphone names, prices, average ratings, number of ratings, memory variants, display features, camera features, and battery capacity. The data is then stored in a CSV file for further analysis.

## Prerequisites
- Python 3.12
- Required libraries: `requests`, `BeautifulSoup` (from `bs4`), `pandas`

## Installation of Required Libraries
Before running the script, ensure that the required libraries are installed. You can install them using `pip`:
```
!pip install requests --upgrade --quiet
```
## Script Breakdown
### 1. Importing Necessary Libraries
The script begins by importing the required libraries:
```
import requests
from bs4 import BeautifulSoup
import pandas as pd
```
- `requests`: Used for making HTTP requests to the Flipkart website.
- `BeautifulSoup`: A parsing library used to extract data from HTML documents.
- `pandas`: Utilized for data manipulation and storage in a CSV file.
<br />

### 2. Sending HTTP Request and Checking Status Code
The script sends a GET request to the Flipkart search URL to retrieve HTML content:
The 200 status code means that the request was successful.
```
url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3D10000&p%5B%5D=facets.price_range.to%3D30000&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock"

response = requests.get(url)
```
<br />

### 3. Parsing HTML Content using BeautifulSoup

```
soup = BeautifulSoup(response.text,'html.parser')
```
<br />

### 4. Extracting Smartphone Data
The script extracts the following data from the HTML:

- #### Smartphone Names:
  ```
  smartphone_divs = soup.find_all('div', class_='KzDlHZ')

  smartphone_name=[]
  for div in smartphone_divs:
      smartphone_name.append(div.text)
  ```
  <br />
  
- #### Prices:<br>
  Extract smartphone prices by finding elements with class `Nx9bqj _4b5DiR`. The script cleans price strings (removes leading rupee symbol and commas), converts them to integers, and appends them to a list
  
  ```
  prices = soup.find_all('div',class_='Nx9bqj _4b5DiR')

  smartphone_price =[]
  for div in prices:
      price_str = div.text[1:].replace(',', '')
      price_int = int(price_str)
      smartphone_price.append(price_int)
  ```
  <br />
  
- #### Average Ratings:
  ```
  rating = soup.find_all('div',class_='XQDdHH')

  smartphone_rating = []
  for div in rating:
      rating_int = float(div.text)
      smartphone_rating.append(rating_int)
  ```
  <br />
  
- #### Number of Ratings:
  ```
  rated_by = soup.find_all('span',class_='Wphh3N')

  number_of_people_rated = []
  for div in rated_by:
      removing_term_ratings = div.text.split(' Ratings')[0]
      removing_comma = removing_term_ratings.replace(',','')
      number_of_people_rated.append(removing_comma)
  ```
  <br />
  
- #### Additional Features (Memory, Display, Camera, Battery):
 ```
 ul_elements = soup.find_all('ul', class_='G4BRas')

 memory = []
 display = []
 camera = []
 battery = []

 for ul in ul_elements:
     li_elements = ul.find_all('li', class_='J+igdf')
   
     memory.append(li_elements[0].text)
     display.append(li_elements[1].text)
     camera.append(li_elements[2].text)
     battery.append(li_elements[3].text)
```
<br />

### 5. Handling Pagination
To scrape data from multiple pages, the script iterates over the specified number of pages (10 in this case):

For each page:
  - Construct the URL for the next page by adding the page number to the base URL.
  - Send a GET request and parse the HTML content.
  - Extract data for smartphone names, prices, ratings, etc., using the same approach as for the first page, appending them to the respective lists.
```
num_pages = 10


for page in range(2, num_pages + 1):
    next_page_url = f"{url}&page={page}"
    response = requests.get(next_page_url)

    soup = BeautifulSoup(response.text,'html.parser')
    smartphone_divs = soup.find_all('div', class_='KzDlHZ')
    
    for div in smartphone_divs:
        smartphone_name.append(div.text)

    prices = soup.find_all('div',class_='Nx9bqj _4b5DiR')
    
    for div in prices:
        price_str = div.text[1:].replace(',', '')
        price_int = int(price_str)
        smartphone_price.append(price_int)

    rating = soup.find_all('div',class_='XQDdHH')
    
    for div in rating:
        rating_int = float(div.text)
        smartphone_rating.append(rating_int)

    rated_by = soup.find_all('span',class_='Wphh3N')
    
    for div in rated_by:
        removing_term_ratings = div.text.split(' Ratings')[0]
        removing_comma = removing_term_ratings.replace(',','')
        number_of_people_rated.append(removing_comma)

    ul_elements = soup.find_all('ul', class_='G4BRas')

    for ul in ul_elements:
        li_elements = ul.find_all('li', class_='J+igdf')
    
        memory.append(li_elements[0].text)
        display.append(li_elements[1].text)
        camera.append(li_elements[2].text)
        battery.append(li_elements[3].text)
```
<br />

### 6. Data Validation
After scraping, the script validates that the number of extracted items is consistent across all attributes:
```
print(len(smartphone_name))
print(len(smartphone_price))
print(len(smartphone_rating))
print(len(number_of_people_rated))
print(len(memory))
print(len(display))
print(len(camera))
print(len(battery))
```
<br />

### 7. Storing Data in a CSV File
The final step involves storing the extracted data in a CSV file using pandas:

1. Create a dictionary `data` with the extracted information as keys and the corresponding lists as values.
2. Create a pandas DataFrame `df` from the dictionary.
3. Export the DataFrame to a CSV file named "flipkart_smartphones_scraped_data.csv".

```
data = {
    'Smartphone Name': smartphone_name,
    'Price (Rs.)': smartphone_price,
    'Average Rating': smartphone_rating,
    'Number of Ratings': number_of_people_rated,
    'Memory Variant': memory,
    'Display Features': display,
    'Camera Features': camera,
    'Battery Features': battery
}

df = pd.DataFrame(data)
df.to_csv('flipkart_smartphones_scraped_data.csv', index=False)

```

## Limitations
- Dynamic Content: The script may not work correctly if Flipkart changes its HTML structure or if the content is dynamically loaded via JavaScript.
- Rate Limiting: Excessive requests in a short time may result in your IP being blocked.
- Data Consistency: Ensure that the number of items scraped per attribute is consistent across all pages.
- Respect Website Resources: Scraping large amounts of data can overload websites. Use this script responsibly and ethically.

## Customization

- You can modify the script to scrape additional data or filter by different criteria.
- Adjust the number of pages to scrape by changing the `num_pages` variable.
- Modify the script to handle potential errors and edge cases.
  
## Conclusion
This script provides an efficient way to scrape smartphone data from Flipkart, but users should be aware of potential limitations and ethical considerations related to web scraping.

