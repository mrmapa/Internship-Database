from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe")
def loadAccentureJobs(searchTerm, driver): # extracts jobInfo from Accenture website through webdriver
    driver.get('https://www.accenture.com/us-en/careers/jobsearch')
    jobSearchBox = driver.find_element_by_id("job-search-hero-bar")
    jobSearchBox.send_keys(searchTerm)
    searchButton = driver.find_element_by_class_name(class_="btn-primary col-xs-12")
    searchButton.click()
    """
    jobSearchBox.click()
    jobSearchBox.send_keys(Keys.ENTER)
    """
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(class_="upper-set-jobs job-listing-block col-xs-12")
    return jobSoup
def extractJobTitleAccenture(jobElem): # extracts job title from web data
    titleElem = jobElem.find('h3', class_="job-title module-title corporate-bold")
    title = titleElem.text.strip()
    return title
def extractJobLocationAccenture(jobElem): # extracts job location from web data
    locationElem = jobElem.find('p', class_="small ucase job-location")
    location = locationElem.text.strip()
    return location
def extractJobDateAccenture(jobElem): # extracts job posting date from web data
    dateElem = jobElem.find('p', class_="posted-date small acn-italic")
    date = dateElem.text.strip()
    return date
def extractJobLinkAccenture(jobElem): # extracts link from web data
    link = jobElem.find('a')['href']
    return link
def saveJobsToExcel(jobsList, filename): # update based on what format we want
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)
def findJobsFrom(website, searchTerm, desiredCharacs, filename="AccentureJobs.xlsx"): # loads Accenture website, extracts data and saves it
    if website == 'Accenture':
        jobSoup = loadAccentureJobs(searchTerm, driver)
        jobsList, numListings = extractJobInformationAccenture(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
        print('{} new job postings retrieved. Stored in {}.'.format(numListings, filename))
def extractJobInformationAccenture(jobSoup, desiredCharacs): # extracts data by searching for desired information per job
    jobElems = jobSoup.find_all(class_="module job-card-wrapper col-md-4 col-xs-12 col-sm-6 corporate-regular background-white")
    cols = [] # creates array of columns
    extractedInfo = [] # creates array of info
    if 'titles' in desiredCharacs: # if titles in desired characs, creates title array and appends it to cols array, appends title data to info array
        titles = []
        cols.append('Titles')
        for jobElem in jobElems:
            titles.append(extractJobTitleAccenture(jobElem))
        extractedInfo.append(titles)
    if 'locations' in desiredCharacs: # if locations in desired characs, creates locations array and appends it to cols array, appends title data to info array
        locations = []
        cols.append('Locations')
        for jobElem in jobElems:
            locations.append(extractJobLocationAccenture(jobElem))
        extractedInfo.append(locations)
    if 'dates' in desiredCharacs: # if dates in desired characs, creates dates array and appends it to cols array, appends title data to info array
        dates = []
        cols.append('Dates')
        for jobElem in jobElems:
            dates.append(extractJobDateAccenture(jobElem))
        extractedInfo.append(dates)
    if 'links' in desiredCharacs: # if links in desired characs, creates links array and appends it to cols array, appends title data to info array
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractJobLinkAccenture(jobElem))
        extractedInfo.append(links)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j]
    numListings = len(extractedInfo[0])
    return jobsList, numListings
desiredCharacs = ['titles', 'locations', 'dates', 'links']
findJobsFrom('Accenture', 'summer intern', desiredCharacs)