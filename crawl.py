

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import MySQLdb
# import pymysql
# pymysql.install_as_MySQLdb()


# 크롤링할 웹 페이지 URL
# url = 'http://example.com'

conn = MySQLdb.connect(
    user="ureca",
    passwd="ureca",
    host="127.0.0.1",
    port=3306,
    db="ureca",
)


cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS CU")
cursor.execute("CREATE TABLE CU (no int primary key, name CHAR(20), img CHAR(100), price CHAR(20))")


driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.get('https://pocketcu.co.kr/product?cate1=0087&cate2=0457')
last_height = driver.execute_script("return document.body.scrollHeight")  
TIME_SLEEP = 6
idx = 1

while True :
    time.sleep(TIME_SLEEP)

    title = driver.find_elements(By.CLASS_NAME, 'prd_set')
    for i in title:
        
        name = i.find_elements(By.CLASS_NAME, 'name')
        img = i.find_element(By.CLASS_NAME, 'lazy')
        price = i.find_element(By.CLASS_NAME, 'price')
        real_price = price.find_element(By.CSS_SELECTOR, 'p')
        
        cursor.execute("INSERT INTO CU VALUES (%s, %s, %s, %s)", (idx, name[0].text, img.get_attribute('src'), real_price.text))
        print(idx);
        print(name[0].text)
        print(img.get_attribute('src'))
        print(real_price.text)

        idx += 1    

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_SLEEP)                                            
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(TIME_SLEEP)

    new_height = driver.execute_script("return document.body.scrollHeight")
    conn.commit()

    if new_height == last_height:                                              
        conn.close()
        break

    last_height = new_height

