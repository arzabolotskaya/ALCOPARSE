import csv
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from model import Content
from bs4 import BeautifulSoup
import re
import time

driver = webdriver.Chrome()
URL = 'https://winestreet.ru/catalog/' #!
HEADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36", "accept" : "*/*"} 
HOST = 'https://winestreet.ru/'
PATH = r'Documents\прога питон 1\прога проект парсер\winestreer.csv' #r нужен так как иначе включается экранирование и \b читается как \x08

class ProgHubParser(object):

    def __init__(self, driver):
        self.driver = driver

    def parse(self):
        links = self.get_all_links()
        all_alkogol = []
        for link in links:
            pages = self.get_all_pages(link)
            print(f'parsing page 1 from {pages}')
            alkogol = self.parse_content_page(link)
            all_alkogol.extend(alkogol) 
            if pages != 1:
                for i in range (pages-1):
                    print(f'parsing page {i+2} from {pages}')
                    next_page = link + f"?page={i+2}"
                    alkogol = self.parse_content_page(next_page)
                    all_alkogol.extend(alkogol)
        return all_alkogol

    def parse_content_page(self, url):
        self.driver.get(url)
        time.sleep(5)


        cards = self.driver.find_elements_by_class_name("cl_info") 
        print(cards)
        alkogol = []
        for card in cards:
            content = Content()

            try:
                content_category_elm = self.driver.find_element_by_tag_name("h1")
                content.category = content_category_elm.text
                print(content.category)
            except NoSuchElementException:
                print("product category missing")


            try:
                content_name_elm = card.find_element_by_class_name("goods_name").find_element_by_tag_name("a")
                content.name = content_name_elm.text
                print(content.name)
            except NoSuchElementException:
                print("product name missing")


            try:
                content_link_elm = card.find_element_by_class_name("goods_name").find_element_by_tag_name("a").get_attribute("href")
                content.link = content_link_elm
                print(content.link)
            except NoSuchElementException:
                print("product link missing")


            try:
                content_price_elm = card.find_element_by_class_name("cl_price").find_element_by_tag_name("span")
                content.price = content_price_elm.text
                print(content.price)
            except NoSuchElementException:
                pass

            try:
                content_sale_elm = card.find_element_by_class_name("cl_price_action").find_element_by_tag_name("span")
                content.sale = content_sale_elm.text
                print(content.sale)
            except NoSuchElementException:
                content.sale = "Нет скидки"

            item = str(content)
            row = item.split(",")
            print(row)
            alkogol.append({
                'type' : row[0],
                'title' : row[-5],
                'link': row[-4],
                'price': row[-3],
                'sale' : row[-2],
                'availability': row[-1] 
                })
        return alkogol 

        



    def get_all_pages(self, url):
        self.driver.get(url)
        print(url)
        time.sleep(5)
        try:
            last_page = self.driver.find_element_by_class_name("pagination").find_elements_by_tag_name("li")[-2].text
            print(last_page)
        except NoSuchElementException:
            print("sorry")
            last_page = 1
        
        return int(last_page)

        


    def get_all_links(self):
        self.driver.get(URL)
        elems = self.driver.find_element_by_class_name("left_sidebar").find_elements_by_tag_name("a")
        all_links = []
        alco_categories = ["https://winestreet.ru/vodka/", "https://winestreet.ru/wine/", "https://winestreet.ru/champagne-and-sparkling-wines/", "https://winestreet.ru/cognac/", "https://winestreet.ru/wiskey/", "https://winestreet.ru/rom/", "https://winestreet.ru/liqueur/", "https://winestreet.ru/beer/", "https://winestreet.ru/gin/", "https://winestreet.ru/tequila/", "https://winestreet.ru/vermut/", "https://winestreet.ru/absent/", "https://winestreet.ru/low-alcohol/"]
        for elem in elems:
            category_link = elem.get_attribute('href')
            category = elem.text
            if category_link in alco_categories:
                all_links.append(category_link)
        print(all_links)
        return all_links


def unify_price(raw_price):
    #Если надо представить цены в виде числа
    clean_price = ''.join(x for x in raw_price if x.isdigit())
    return int(clean_price)




def main():
    #soup = BeautifulSoup(html, 'html.parser')
    #items = soup.find('div', class_='category-preview__header')
    driver = webdriver.Chrome()
    parser = ProgHubParser(driver)
    all_alkogol = parser.parse()
    
    save_file(all_alkogol, PATH)



def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вид', 'Наименование', "Ссылка", "Цена", "Старая цена", "Наличие"]) #!
        for item in items:
            writer.writerow([item['type'], item['title'], item['link'], item['price'], item['sale'], item['availability']]) #!

print(main())










def fill_content_category(self, content):
    try:
        content_name_elm = card.find_element_by_class_name("catalog-list-item articles-selector js-catalog-item").get_attribute("data-category")
        content.category = content_category_elm.text
    except NoSuchElementException:
        print("product category missing")

def fill_content_name(self, content):
    try:
        content_name_elm = card.find_element_by_class_name("catalog-list-item articles-selector js-catalog-item").get_attribute("data-name")
        content.name = content_name_elm.text
    except NoSuchElementException:
        print("product name missing")

def fill_content_link(self, content):
    try:
        content_name_elm = card.find_element_by_class_name("catalog-list-item__image js-product-detail-link").get_attribute("href")
        content.link = content_link_elm
    except NoSuchElementException:
        print("product link missing")

def fill_content_price(self, content):
    try:
        content_name_elm = card.find_element_by_class_name("catalog-list-item articles-selector js-catalog-item").get_attribute("data-price")
        content.price = content_price_elm.text
    except NoSuchElementException:
        pass

def load_more():
    try:
        btn = self.driver.find_element_by_class_name("control-button control-button--load-more")
        print('btn[load more]:', btn,'\n')
        ActionChains(driver).move_to_element(btn).click(btn).perform()
        print('btn is clicked')
    except Exception as e:
        print('Click Error:', e)
    click = input('want more to click? (y/n)')
    if click != 'y':
        pass