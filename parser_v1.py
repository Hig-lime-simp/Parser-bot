
# Этот парсер берет инфу со всей страници, по идее это не оптимизировано

import json
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup as bs
import time

url = "https://public-api.reviews.2gis.com/3.0/branches/70000001056730848/reviews?limit=50&offset=0&is_advertiser=false&fields=meta.providers,meta.branch_rating,meta.branch_reviews_count,meta.total_count,reviews.hiding_reason,reviews.emojis,reviews.trust_factors&rated=true&sort_by=trust&key=6e7e1929-4ea9-4a5d-8c05-d601860389bd&locale=ru_RU"



def init(): # Инициализация скрипта + первый прогон парсера и сохранение данных в json
    driver = init_driver()
    html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.726081%2C48.804554%2F16")
    title = get_title("._19h0cqe", html)
    dis = get_discription("._83kmcy", html)
    arr =  compilation_json(title, dis)
    return arr, driver, title

def compilation_json(title, discription): # Функция по сбору json паралельной записью в массив
    arr = []
    for i in range(0, len(title)):
          arr.append([title[i], discription[i]])
    return arr

def get_discription(class_name, html): # Простой поиск по имени класса
     ListOfDis = []
     for block_of_discription in html.select(class_name):
          dis = block_of_discription.find("a")
          ListOfDis.append(dis.text)
     return ListOfDis

def get_title(class_name, html): # Простой поиск по имени класса
     ListOfTitle = []
     for title in html.select(class_name):
          ListOfTitle.append(title.text)
     return ListOfTitle

def get_review(driver, url): # GET на сайт + обратока BS
     driver.get(url)
     html = bs(driver.page_source, "html.parser")
     return html

def init_driver(): # Инициализация драйвера + параметры для запуска имитации бразера
    driver = webdriver.Chrome()
    stealth(driver,
            languages=["ru","ru-RU"],
            vendor="Google Inc",
            webgl_vendor="Intel Inc",
            renderer="Intel Iris OpenGL Engine",
            platform="Win32"
            )
    return driver

# if __name__ == "__main__":

ForPostJSon, driver, old_data = init()

with open('data.json', 'w', encoding='utf-8') as f:
     json.dump(ForPostJSon, f, ensure_ascii=False, indent=4)
f.close()

while True:
     New_html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.726081%2C48.804554%2F16")
     new_data = get_title("._19h0cqe", New_html)

     if old_data == new_data: # Сравнение полученых title с сохранеными для оптимизации запросов
          time.sleep(900)
     else:
          ForPostJSon = compilation_json(new_data, get_discription("._83kmcy", New_html))

          old_data = new_data

          with open('data.json', 'w', encoding='utf-8') as f:
               json.dump(ForPostJSon, f, ensure_ascii=False, indent=4)
          f.close()
          time.sleep(900)
