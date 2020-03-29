import csv
#from datetime import datetime
import requests 
from bs4 import BeautifulSoup
import re


URL = 'https://bristol.ru/catalog/alkogol/'
HEADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36", "accept" : "*/*"} 
HOST = 'https://bristol.ru/'
PATH = r'Documents\прога питон 1\прога проект парсер\bristol.alkogol.csv' #r нужен так как иначе включается экранирование и \b читается как \x08

def remove_html_tags(text):
    #Если надо достать текст между html тегами другим способом
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def unify_price(raw_price):
    #Если надо представить цены в виде числа
    clean_price = ''.join(x for x in raw_price if x.isdigit())
    return int(clean_price)

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params = params) 
    return r 

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_ = 'btn pag-btn')
    print(pagination[-1])
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="holder elements")
    alkogol = []
    for item in items:
        prices = item.find_all('span', class_ = 'catalog-price')
        if len(prices) == 1: 
            price_text = item.find('span', class_ = "catalog-price").get_text()
            price_value = unify_price(price_text)
            old_value = "Это изначальная цена"
        else:
            old_text = item.find('span', class_ = 'catalog-price old').get_text()
            old_value = unify_price(old_text)
            price_text = item.find('span', class_ = "catalog-price new").get_text()
            price_value = unify_price(price_text)

        alkogol.append({
            'type' : "Крепкий алкоголь",
            'title' : item.find('div', class_ = "catalog-title").get_text(strip = True),
            'link': HOST + item.find('div', class_ = "catalog-title").find_next('a').get('href'),
            'price': price_value,
            'sale' : old_value,
            'availability': 'В наличии' #item.find('div', class_ = "views-field-field-available-value").get_text(strip = "\n")
        })

    return alkogol

def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вид', 'Наименование', "Ссылка", "Цена", "Старая цена", "Наличие"])
        for item in items:
            writer.writerow([item['type'], item['title'], item['link'], item['price'], item['sale'], item['availability']])


def parse(url):
    html = get_html(url)
    print(f"{html.status_code} -- {url}")


    
    if html.status_code == 200:
        alkogol = []
        
        pages_count = get_pages_count(html.text)
        print(pages_count)
        for page in range(1, pages_count + 1):
            print(f'Parsing {page} from {pages_count}')
            html = get_html(url, params={'PAGEN_1' : page})
            if html.status_code == 200:
                alkogol.extend(get_content(html.text))
            else:
                print(f"Error on page {page}")
        print(f'Total {len(alkogol)}')
        
        save_file(alkogol, PATH)
      

    else:
        print("Error")
    
    return alkogol


        #Если надо проверить, куда я сохранила файл:
        #import os
        #print(os.path.abspath("bonvi.csv"))

print(parse(URL))
