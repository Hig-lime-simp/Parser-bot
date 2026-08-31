
# Этот парсер должен будет вычлинять дивы с одного контейнера, class="_qvsf7z", вот по идее контейнер содержащий все отзовы

import requests
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup as bs
import time

def get_review(driver, url):
     driver.get(url)
     html = bs(driver.page_source, "html.parser")

     return html

def init():
    driver = webdriver.Chrome()
    stealth(driver,
            languages=["ru","ru-RU"],
            vendor="Google Inc",
            webgl_vendor="Intel Inc",
            renderer="Intel Iris OpenGL Engine",
            platform="Win32"
            )
    return driver

driver = init()

list_review = []

i = 0

html = get_review(driver, "https://2gis.ru/volzhsky/firm/70000001056730848/tab/reviews?m=44.725975%2C48.804477%2F19.88")

for review in html.select("._1rowqpjv"):
      print()
    # title = review.select("._19h0cqe")
    # for title in review.select("._19h0cqe"):
    #     print(title.text)
    # discrition = review.find("p", class_="review-card-text").text
    # list_review.append([title,discrition])
# else:
#     for i in list_review:
#         print(f'Загаловок: {i[0]}, Описание {i[-1]}')
for title in html.select("._19h0cqe"):
        print(title.text)