import time
import os
from selenium import webdriver
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe")
driver.get('https://www.google.com/')
time.sleep(5)
driver.close()
