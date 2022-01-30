import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def loadGoogleJobs(searchTerm): # loads web data from Google Careers website given searchTerm
    url = "https://careers.google.com/jobs/results/?distance=50&hl=en_US&jlo=en_US&q=" + searchTerm
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobSoup = soup.find('ol', id="search-results")
    print(jobSoup)
    return jobSoup
loadGoogleJobs("summer intern")
""""
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
"""""