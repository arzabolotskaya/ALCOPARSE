import requests, csv
from bs4 import BeautifulSoup
import re
import time

URL = "https://www.globus.ru/catalog/alkogol/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36', 'accept': '*/*'}
HOST = "https://www.globus.ru"
FILE = "globus.csv"
#proxies = {'https' : '163.172.182.164', 'https':'163.172.168.124', 'https':'188.170.233.104', 'https':'177.87.39.104'}


def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params) #timeout=3)
    time.sleep(2)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_ = "navigation js-navigation").find_all('a', class_ = "paging")[-2].get('href')
    total_pages = int(pages.split('=')[-1])
    return total_pages

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("a", class_ = "pim-list__item ga-event")
    alkogol =[]
    for item in items:
        categ = item.find('div', class_ ="pim-list__item-title").get_text(strip = True).split(' ')[0]
        title = item.find('div', class_ = "pim-list__item-title").get_text(strip = True)
        link = HOST + item.get('href')
        pricenewr = item.find('span', class_ = 'pim-list__item-price-actual-main').get_text(strip = True)
        pricenewk=item.find('span', class_ = 'pim-list__item-price-actual-sub').get_text(strip = True)
        pricenew = pricenewr+','+pricenewk
        pricer = item.find('span', class_='pim-list__item-price-old-main')
        if pricer != None:
            pricer1 = pricer.get_text(strip=True)
            pricek = item.find('span', class_='pim-list__item-price-old-sub').get_text(strip=True)
            price = pricer1 +','+pricek
            cond = item.find('div', class_ = 'pim-list__date-active-price').get_text(strip=True).split()
            cond1 = ' '.join(cond)
        else:
            price = "На данный товар нет акций"
            cond1 = ''

        alkogol.append({
            'category': categ,
            'title': title,
            'link': link,
            'price': price,
            'new_price':pricenew,
            'cond':cond1
        })

    return alkogol

def save_file(items, path):
    with open (path, 'w', newline = '') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(['Вид','Название', 'Ссылка', 'Цена', 'Старая цена/наличие','Условия'])
        for item in items:
            writer.writerow([item['category'],item['title'], item['link'], item['new_price'], item['price'], item['cond']])



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




