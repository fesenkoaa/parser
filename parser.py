import requests
from bs4 import BeautifulSoup
import csv

from config import user_agent

HOST = 'https://www.otomoto.pl/'
URL = 'https://www.otomoto.pl/osobowe/bmw/m5/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': user_agent
}
FILE = 'cars2.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="offer-item__wrapper")

    cars = []
    for item in items:
        cars.append({
            'title': item.find('a', class_='offer-title__link').get_text('title', strip=True),
            'year': item.find('li', attrs={'data-code': 'year'}).get_text(strip=True),
            'mileage': item.find('li', attrs={'data-code': 'mileage'}).get_text(strip=True),
            'price': item.find('span', class_='offer-price__number ds-price-number').get_text(strip=True),
            'city': item.find('span', class_='ds-location-city').get_text(strip=True),
            'link': item.find('a', class_='offer-title__link').get('href')
        })
    return cars


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'year', 'mileage', 'price', 'city', 'link'])
        for item in items:
            writer.writerow([item['title'], item['year'], item['mileage'], item['price'], item['city'], item['link']])


def parser():
    html = get_html(URL)

    if html.ok:
        cars = []
        pages = get_pages(html.text)
        for page in range(1, pages + 1):
            print(f'Parsing of page {page} of pages...')
            html = get_html(URL, params={'page': page}).text
            cars.extend(get_content(html))
        save(cars, path=FILE)
        print(f'Got {len(cars)}')
    else:
        print(html.status_code)


parser()
