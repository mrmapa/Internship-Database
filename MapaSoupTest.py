import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

#test
def load_indeed_jobs_div(job_title, location):
    getVars = {'q' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    print(job_soup)
    return job_soup

def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_="jobTitle")
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_="companyName")
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.indeed.com/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_="date")
    date = date_elem.text.strip()
    return date

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)

def find_jobs_from(website, job_title, location, desired_characs, filename="results.xlsx"):
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)

        save_jobs_to_excel(jobs_list, filename)

def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_="slider_container")

    cols = []
    extracted_info = []
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])
    return jobs_list, num_listings

desired_characs = ['titles', 'companies', 'links', 'date_listed']
find_jobs_from('Indeed', 'data science intern', 'United States', desired_characs)