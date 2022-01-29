import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def load_google_jobs_div(job_title, location):
    getVars = {'q' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://careers.google.com/jobs/results/?distance=50&q=summer%202022' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="search-results")
    return job_soup

def extract_job_title_google(job_elem):
    title_elem = job_elem.find('h2', class_ = 'gc-card__title gc-heading gc-heading--beta')
    title = title_elem.text.strip()
    return title

def extract_company_google(job_elem):
    company_elem = job_elem.find('span', class_ = 'gc-icon')
    company = company_elem.text.strip()
    return company

def extract_link_google(job_elem):
    link = job_elem.find('a')['href']
    link = '/jobs/results/126403584381067974-research-intern-ms-summer-2022/?distance=50&q=summer%202022' + link
    return link

def extract_date_google(job_elem):
    date_elem = job_elem.find('span', class_= 'gc-card')