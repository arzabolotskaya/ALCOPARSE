import csv
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from model import Content
from bs4 import BeautifulSoup
import re



URL = 'https://krasnoeibeloe.ru/catalog/' #!
HEADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36", "accept" : "*/*"} 
HOST = 'https://krasnoeibeloe.ru/'
PATH = r'Documents\прога питон 1\прога проект парсер\krasnoeibeloe.csv' #r нужен так как иначе включается экранирование и \b читается как \x08

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
            print(alkogol)
            if pages != 1:
                for i in range (pages-1):
                    print(f'parsing page {i+2} from {pages}')
                    next_page = self.driver.find_element_by_class_name("pag_arrow_right").find_element_by_tag_name("a").get_attribute("href")
                    alkogol = self.parse_content_page(next_page)
                    all_alkogol.extend(alkogol)
                    print(alkogol)
        return all_alkogol

    def parse_content_page(self, url):
        self.driver.get(url)
        cards = self.driver.find_elements_by_class_name("catalog_product_item_cont")
        alkogol = []
        for card in cards:
            content = Content()

            try:
                content_category_elm = self.driver.find_element_by_class_name("cont_right_col").find_element_by_tag_name("h1")
                content.category = content_category_elm.text
            except NoSuchElementException:
                print("product category missing")

            try:
                content_name_elm = card.find_element_by_class_name("product_item_name").find_element_by_tag_name("a")
                content.name = content_name_elm.text
            except NoSuchElementException:
                print("product name missing")

            try:
                content_link_elm = card.find_element_by_class_name("product_item_name").find_element_by_tag_name("a").get_attribute('href')
                content.link = content_link_elm
            except NoSuchElementException:
                print("product link missing")
            
            try:
                content_price_elm = card.find_element_by_class_name("i_price").find_element_by_tag_name("div")
                content.price = content_price_elm.text
            except NoSuchElementException:
                content.availability = "not avilable"

            item = str(content)
            row = item.split(",")
            
            print(row)
            alkogol.append({
                'type' : row[0],
                'title' : row[-4],
                'link': row[-3],
                'price': row[-2],
                'sale' : " ",
                'availability': row[-1] 
                })
        return alkogol 

        
    def get_all_pages(self, url):
        self.driver.get(url)
        print(url)
        try:
            last_page = self.driver.find_element_by_class_name("bl_pagination").find_elements_by_tag_name("a")[-2].text
        except NoSuchElementException:
            last_page = 1
        
        return int(last_page)

        


    def get_all_links(self):
        self.driver.get(URL)
        elems = self.driver.find_elements_by_class_name("catalog_top_sections__item__name")
        all_links = []
        alco_categories = ["https://krasnoeibeloe.ru/catalog/__2/", "https://krasnoeibeloe.ru/catalog/vino-s-otsenkoy/", "https://krasnoeibeloe.ru/catalog/vodka_nastoyki/", "https://krasnoeibeloe.ru/catalog/viski/", "https://krasnoeibeloe.ru/catalog/konyak_armanyak_brendi/", "https://krasnoeibeloe.ru/catalog/rom_jin_tequila_liquor/", "https://krasnoeibeloe.ru/catalog/importnoe_pivo/", "https://krasnoeibeloe.ru/catalog/rossiyskoe/", "https://krasnoeibeloe.ru/catalog/__7/"]
        for elem in elems:
            category_link = elem.find_element_by_tag_name('a').get_attribute('href')
            category = elem.find_element_by_tag_name('a').text
            if category_link in alco_categories:
                all_links.append(category_link)
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
        writer.writerow(['Вид', 'Наименование', "Ссылка", "Цена", "По акции", "Наличие"]) #!
        for item in items:
            writer.writerow([item['type'], item['title'], item['link'], item['price'], item['sale'], item['availability']]) #!

print(main())










def fill_content_category(self, content):
    try:
        content_category_elm = self.driver.find_element_by_class_name("cont_right_col").find_element_by_tag_name("h1")
        content.category = content_category_elm.text
    except NoSuchElementException:
        print("product category missing")

def fill_content_name(self, content):
    try:
        content_name_elm = card.find_element_by_class_name("product_item_name").find_element_by_tag_name("a")
        content.name = content_name_elm.text
    except NoSuchElementException:
        print("product name missing")

def fill_content_link(self, content):
    try:
        content_link_elm = self.driver.find_element_by_class_name("product_item_name").find_element_by_tag_name("a").get_attribute('href')
        content.link = content_link_elm
    except NoSuchElementException:
        print("product дштл missing")

def fill_content_price(self, content):
    try:
        content_price_elm = self.driver.find_element_by_class_name("i_price").find_element_by_tag_name("div")
        content.price = content_price_elm.text
    except NoSuchElementException:
        pass
