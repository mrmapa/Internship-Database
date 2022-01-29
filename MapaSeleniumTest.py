import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

def initiateDriver(locationOfDriver, browser):
    if browser == 'chrome':
