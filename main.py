import csv
#from datetime import datetime
import requests 
from bs4 import BeautifulSoup
import re

#особенно парсить вино, виски, крепленые вина и прочие см line 110

URL = 'https://bristol.ru/catalog/pivo/'
HEADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36", "accept" : "*/*"} 
HOST = 'https://bristol.ru/'
PATH = r'Documents\прога питон 1\прога проект парсер\bristol.csv' #r нужен так как иначе включается экранирование и \b читается как \x08

def remove_html_tags(text):
    #Если надо достать текст между html тегами другим способом
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def unify_price(raw_price):
    #Если надо представить цены в виде числа
    clean_price = ''.join(x for x in raw_price if x.isdigit())
    return int(clean_price)

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params = params) #response = urllib.requests.urlopen(url)
    return r #response.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='top-mobile-menu__item')
    links = []
    alco_categories = ("Пиво", "Вина", "Шампанское", "Алкоголь")
    for item in items:
        link = HOST + item.find('a').get('href')
        category = item.get_text(strip = True)
        if category in alco_categories:
            links.append(link)
    return links

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_ = 'pager-item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="holder elements")
    alkogol = []
    for item in items:
        price_text = item.find('span', class_ = "catalog-price").get_text()
        price_value = unify_price(price_text)
        alkogol.append({
            'type' : "Пиво",
            'title' : item.find('div', class_ = "catalog-title").get_text(strip = True),
            'link': HOST + item.find('div', class_ = "catalog-title").find_next('a').get('href'),
            'price': price_value,
            'availability': item.find('div', class_ = "views-field-field-available-value").get_text(strip = "\n")
        })

    return alkogol

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вид', 'Наименование', "Ссылка", "Цена", "Наличие"])
        for item in items:
            writer.writerow([item['type'], item['title'], item['link'], item['price'], item['availability']])


def parse(url):
    html = get_html(url)
    print(f"{html.status_code} -- {url}")


    
    if html.status_code == 200:
        alkogol = []
        
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing {page} from {pages_count}')
            html = get_html(url, params={'page' : page})
            if html.status_code == 200:
                alkogol.extend(get_content(html.text))
            else:
                print(f"Error on page {page}")
        print(f'Total {len(alkogol)}')
        
        
      

    else:
        print("Error")
    
    return alkogol

def main():
    html = get_html(URL)
    print(html.status_code)
    
    if html.status_code == 200:
        all_alkogol = []
        all_alkogol.extend(parse(html.text))

        save_file(all_alkogol, PATH)

        #Если надо проверить, куда я сохранила файл:
        #import os
        #print(os.path.abspath("bonvi.csv"))

print(main())
