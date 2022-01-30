from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe")
def loadMetaJobs(searchTerm, driver): # extracts jobInfo from Meta website through webdriver
    driver.get("https://www.facebookcareers.com/jobs/?q=" + searchTerm)
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(class_="_8tk7")
    return jobSoup
def extractJobTitleMeta(jobElem): # extracts job title from web data
    titleElem = jobElem.find(class_="_8sel _97fe")
    title = titleElem.text.strip()
    return title
def extractJobLocationMeta(jobElem): # extracts job location from web data
    locationElem = jobElem.find(class_="_8see _97fe")
    location = locationElem.text.strip()
    return location
"""
def extractJobLinkMeta(jobElem): # extracts job link from web data
    link = "facebookcareers.com" + jobElem.find('a')['href']
    return link
"""
def saveJobsToExcel(jobsList, filename): # update based on what format we want
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)
def findJobsFrom(website, searchTerm, desiredCharacs, filename="MetaJobs.xlsx"): # loads Bloomberg website, extracts data and saves it
    if website == 'Meta':
        jobSoup = loadMetaJobs(searchTerm, driver)
        jobsList, numListings = extractJobInformationMeta(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
        print('{} new job postings retrieved. Stored in {}.'.format(numListings, filename))
def extractJobInformationMeta(jobSoup, desiredCharacs): # extracts data by searching for desired information per job
    jobElems = jobSoup.find_all(class_="_8sef")
    cols = []  # creates columns array
    extractedInfo = []  # creates array of info
    company = []
    cols.append('Company')
    for jobElem in jobElems:
        company.append("Meta")
    extractedInfo.append(company)
    if 'titles' in desiredCharacs:  # if titles in desired characs, creates title array
        titles = []
        cols.append('Titles')
        for jobElem in jobElems:
            titles.append(extractJobTitleMeta(jobElem))
        extractedInfo.append(titles)
    if 'locations' in desiredCharacs:  # if locations in desired characs, creates locations array
        locations = []
        cols.append('Locations')
        for jobElem in jobElems:
            locations.append(extractJobLocationMeta(jobElem))
        extractedInfo.append(locations)
    """
    if 'links' in desiredCharacs:  # if links in desired characs, creates links array
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractJobLinkMeta(jobElem))
        extractedInfo.append(links)
    """
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j]
    numListings = len(extractedInfo[0])
    return jobsList, numListings
desiredCharacs = ['titles', 'locations']
findJobsFrom('Meta', 'summer intern', desiredCharacs)