import requests, csv
from bs4 import BeautifulSoup
import re

URL = "https://www.perekrestok.ru/catalog/alkogol"
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'accept': '*/*'}
HOST = "https://www.perekrestok.ru"
URL1 = "https://www.perekrestok.ru/catalog/alkogol?page=1&sort=rate_desc"
FILE = "perek.csv"

def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("li", class_ = "js-catalog-product")
    alkogol =[]
    for item in items:
        t = item.find('div', class_ = "xf-product__cost xf-product-cost")
        if t != None:
            p = t.find('div', class_='xf-price').get('data-quantum-cost')
        else:
            p = "Товар временно отсутствует"
        alkogol.append({
            'category': item.find('div', class_ ="xf-product").get('data-gtm-category-name'),
            'title': item.find('div', class_ = "xf-product__title xf-product-title").get_text(strip = True),
            'link': HOST + item.find('a', class_="xf-product-title__link").get('href'),
            'price': p
        })

    return alkogol

def save_file(items, path):
    with open (path, 'w', newline = '') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(['Вид','Название', 'Ссылка', 'Цена'])
        for item in items:
            writer.writerow([item['category'],item['title'], item['link'], item['price']])


def get_page(url):
    page = 1
    while True:
        perek = requests.get(url)
        if not str(perek.status_code).startswith('2'):
            print("smth went bad for url ", url)

        soup = BeautifulSoup(perek.text, 'html.parser')
        possible_next_links = soup.find_all("a",
                                            class_="xf-paginator__item js-paginator__next")
        if not possible_next_links:
            return page

        else:
            for possible_link in possible_next_links:
                possible_url = possible_link.get("href", None)
                if possible_url:
                    url = possible_url
                    next_page_num_match = re.search(r"\?page=(?P<pageNum>\d+)", url)
                    if next_page_num_match:
                        next_page_num = int(next_page_num_match.group("pageNum"))
                        page = next_page_num
                    break


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        alkogol = []
        alkogol.extend(get_content(html.text))
        pages = get_page(URL1)
        for page in range(1, pages + 1):
            print('Парсинг страницы', page, 'из', pages)
            html = get_html(URL, params={'page': page})
            p=get_content(html.text)
            alkogol.extend(p)
        save_file(alkogol, FILE)
    else:
        print('Error')


parse()




