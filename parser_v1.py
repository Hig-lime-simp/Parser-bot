
# Этот парсер берет инфу со всей страници, по идее это не оптимизировано

import json
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup as bs
import time

def init(): # Инициализация скрипта + первый прогон парсера и сохранение данных в json
    driver = init_driver()
    html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.725975%2C48.804477%2F19.88")
    title = get_title("._19h0cqe", html)
    dis = get_discription("._83kmcy", html)
    arr =  compilation_json(title, dis)
    return arr, driver, title

def compilation_json(title, discription): # Функция по сбору json паралельной записью в словарь
    arr = []
    for i in range(0, len(title)):
          arr.append({title[i]: discription[i]})
    return json.dumps(arr, ensure_ascii=False)

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

ForPostJSon, driver, old_data = init()

while True:
     New_html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.725975%2C48.804477%2F19.88")
     new_data = get_title("._19h0cqe", New_html)

     if old_data == new_data: # Сравнение полученых title с сохранеными для оптимизации запросов
          time.sleep(900)
     else:
          ForPostJSon = compilation_json(new_data, get_discription("._83kmcy", New_html))
          old_data = new_data
          time.sleep(900)
