import requests
from bs4 import BeautifulSoup
import csv

URL = "https://av.ru/g/00095000"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'accept': '*/*'}
HOST = "https://av.ru"
FILE = 'av_nab.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="b-grid__item")
    alkogol = []
    for item in items:
        offer = item.find('span', class_="b-product-tag")
        if offer:
            special_offer = offer.get_text(strip=True).replace('\n', '')
        else:
            special_offer = "На данный товар нет акций"
        alkogol.append({
            'category': 'Наборы',
            'title': item.find('div', class_="b-product__title-block").get_text(strip=True),
            'link': HOST + item.find('a', class_="b-product__title js-list-prod-open").get('href'),
            'price': item.find('div', class_="b-product__price").get('content').replace('\xa0', ''),
            'special_offer': special_offer
        })
    return alkogol


def save_file(items, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Категория', 'Название', 'Ссылка', 'Цена', 'Акции'])
        for item in items:
            writer.writerow([item['category'], item['title'], item['link'], item['price'], item['special_offer']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        alkogol = get_content(html.text)
        save_file(alkogol, FILE)
    else:
        print('Error')


parse()


