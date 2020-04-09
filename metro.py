import requests, csv
from bs4 import BeautifulSoup
from random import choice
import time
import certifi
import urllib3
#proxies = {'https' : '163.172.182.164', 'https':'163.172.168.124', 'https':'188.170.233.104', 'https':'177.87.39.104'}


URL = "https://msk.metro-cc.ru/category/produkty/alkogolnaya-produkciya/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36', 'accept': '*/*'}
HOST = "https://msk.metro-cc.ru"
FILE = "metro.csv"
#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
#headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    time.sleep(2)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_ = "pagination").find_all('a')[-2].get('href')
    total_pages = int(pages.split('=')[3])
    return total_pages

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_ = "catalog-i")
    alkogol =[]
    for item in items:
        categ = item.find('span', class_ ="title").get_text(strip = True).split(' ')[0]
        title = item.find('span', class_ = "title").get_text(strip = True)
        link = item.find('a', class_="catalog-i_link").get('href')
        pricerub = item.find('div', class_ = 'item-price').find('span', class_='int')
        if pricerub != None:
            pricerub=pricerub.get_text().replace(' ', '')
            pricekop = item.find('div', class_ = 'item-price').find('span', class_ = 'float').get_text()
            price = pricerub +','+ pricekop
            nal = "В наличии"
        else:
            price = ''
            nal = 'Нет в наличии'
        salerub = item.find('div', class_ ='opt-price-lvl__price')
        if salerub!= None:
            salerub1 = salerub.find('span', class_='int').get_text().replace(" ", "")
            salekop = item.find('div', class_ ='opt-price-lvl__price').find('span', class_='float').get_text().split()
            salekop1=' '.join(salekop)
            sale = salerub1 + salekop1
            sale_detail = item.find('div', class_='opt-price-lvl__details').get_text(strip= True)
        else:
            sale = "На данный товар нет акций"
            sale_detail = ''

        alkogol.append({
            'category': categ,
            'title': title,
            'link': link,
            'price': price,
            'sale':sale,
            'details': sale_detail,
            'nalichie':nal
        })

    return alkogol

def save_file(items, path):
    with open (path, 'w', newline = '') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(['Вид','Название', 'Ссылка', 'Цена', 'Акции', 'Условия акции', 'Наличие'])
        for item in items:
            writer.writerow([item['category'],item['title'], item['link'], item['price'], item['sale'], item['details'],item['nalichie']])



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        alkogol = []
        alkogol.extend(get_content(html.text))
        pages = get_pages_count(html.text)
        for page in range(1, pages + 1):
            print('Парсинг страницы', page, 'из', pages)
            html = get_html(URL, params={'page': page})
            alkogol.extend(get_content(html.text))

        save_file(alkogol, FILE)
    else:
        print('Error')


parse()



