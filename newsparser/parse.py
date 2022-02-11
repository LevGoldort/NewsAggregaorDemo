import requests
from bs4 import BeautifulSoup

URL = 'https://www.ynetnews.com/category/3089'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('div', class_='slotView')
print(results)
