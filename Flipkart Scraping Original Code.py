


!pip install requests --upgrade --quiet

import requests
from bs4 import BeautifulSoup

import pandas as pd

url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D30000"

response = requests.get(url)

response.status_code

soup = BeautifulSoup(response.text,'html.parser')

smartphone_divs = soup.find_all('div', class_='KzDlHZ')

smartphone_name=[]
for div in smartphone_divs:
    smartphone_name.append(div.text)

prices = soup.find_all('div',class_='Nx9bqj _4b5DiR')

smartphone_price =[]
for div in prices:
    price_str = div.text[1:].replace(',', '')
    price_int = int(price_str)
    smartphone_price.append(price_int)

rating = soup.find_all('div',class_='XQDdHH')

smartphone_rating = []
for div in rating:
    rating_int = float(div.text)
    smartphone_rating.append(rating_int)

discount = soup.find_all('div',class_='UkUFwK')

discount_offered = []
for div in discount:
    disc_str = div.text.replace(' off','')
    discount_offered.append(disc_str)

rated_by = soup.find_all('span',class_='Wphh3N')

number_of_people_rated = []
for div in rated_by:
    removing_term_ratings = div.text.split(' Ratings')[0]
    removing_comma = removing_term_ratings.replace(',','')
    number_of_people_rated.append(removing_comma)

num_pages = 50

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

    discount = soup.find_all('div',class_='UkUFwK')
    
    for div in discount:
        disc_str = div.text.replace(' off','')
        discount_offered.append(disc_str)

    rated_by = soup.find_all('span',class_='Wphh3N')
    
    for div in rated_by:
        removing_term_ratings = div.text.split(' Ratings')[0]
        removing_comma = removing_term_ratings.replace(',','')
        number_of_people_rated.append(removing_comma)