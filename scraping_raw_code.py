!pip install requests --upgrade --quiet

import requests
from bs4 import BeautifulSoup

import pandas as pd

url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3D10000&p%5B%5D=facets.price_range.to%3D30000&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock"

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

rated_by = soup.find_all('span',class_='Wphh3N')

number_of_people_rated = []
for div in rated_by:
    removing_term_ratings = div.text.split(' Ratings')[0]
    removing_comma = removing_term_ratings.replace(',','')
    number_of_people_rated.append(removing_comma)


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

print(len(smartphone_name))
print(len(smartphone_price))
print(len(smartphone_rating))
print(len(number_of_people_rated))
print(len(memory))
print(len(display))
print(len(camera))
print(len(battery))

data = {'Smartphone Name':smartphone_name,'Price (Rs.)':smartphone_price,'Average Rating':smartphone_rating,'Number of Ratings':number_of_people_rated,'Memory Variant':memory,'Display Features':display,'Camera Features':camera,'Battery Features':battery}

df = pd.DataFrame(data)

df.to_csv('flipkart smartphones scraped data.csv', index=False)