
# Этот парсер берет инфу со всей страници, по идее это не оптимизировано

import json
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup as bs
import time

start = time.time()

def init():
    driver = init_driver()
    html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.725975%2C48.804477%2F19.88")
    title = get_title("._19h0cqe", html)
    dis = get_discription("._83kmcy", html)
    arr =  compilation_json(title, dis)
    return arr, driver, title, dis

def compilation_json(title, discription):
    arr = []
    for i in range(0, len(title)):
          arr.append({title[i]: discription[i]})
    return json.dumps(arr, ensure_ascii=False)

def get_discription(class_name, html):
     ListOfDis = []
     for block_of_discription in html.select(class_name):
          dis = block_of_discription.find("a")
          ListOfDis.append(dis.text)
     return ListOfDis

def get_title(class_name, html):
     ListOfTitle = []
     for title in html.select(class_name):
          ListOfTitle.append(title.text)
     return ListOfTitle

def get_review(driver, url):
     driver.get(url)
     html = bs(driver.page_source, "html.parser")
     return html

def init_driver():
    driver = webdriver.Chrome()
    stealth(driver,
            languages=["ru","ru-RU"],
            vendor="Google Inc",
            webgl_vendor="Intel Inc",
            renderer="Intel Iris OpenGL Engine",
            platform="Win32"
            )
    return driver

Json, driver, old_data, old_data_dis = init()
i = 0
while True:
     i += 1
     New_html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.725975%2C48.804477%2F19.88")
     new_data = get_title("._19h0cqe", New_html)

     if old_data == new_data:
          print("Данные не обновились")
          time.sleep(900)
     else:
          ForPostJSon = compilation_json(new_data, get_discription("._83kmcy", New_html))
          old_data = new_data
          print("Данные обновились")
          time.sleep(900)
