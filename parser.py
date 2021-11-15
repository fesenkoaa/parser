import requests
from bs4 import BeautifulSoup
import csv

from config import accept, user_agent


class ParserOtomoto():

    def __init__(self, page_url, headers, filename):
        self.page_url = page_url
        self.headers = headers
        self.filename = filename

    def get_html(self, url, params=None):
        r = requests.get(self.page_url, headers=self.headers, params=params)
        return r

    def get_content(self, html):
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

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('span', class_='page')
        if pagination:
            return int(pagination[-1].get_text())
        else:
            return 1

    def save(self, items, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['title', 'year', 'mileage', 'price', 'city', 'link'])
            for item in items:
                writer.writerow(
                    [item['title'], item['year'], item['mileage'], item['price'], item['city'], item['link']])

    def parser(self):
        html = self.get_html(self.page_url)

        if html.ok:
            cars = []
            pages = self.get_pages(html.text)
            for page in range(1, pages + 1):
                print(f'Parsing of page {page} of {pages}...')
                html = self.get_html(self.page_url, params={'page': page}).text
                cars.extend(self.get_content(html))
            self.save(cars, path=self.filename)
            print(f'Got {len(cars)}')
        else:
            print(html.status_code)


# m5 = ParserOtomoto('https://www.otomoto.pl/osobowe/bmw/m5/', {'accept': accept, 'user-agent': user_agent}, 'cars.csv')
# m5.parser()

