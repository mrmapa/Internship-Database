from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe")
def loadGoogleJobs(searchTerm, driver): # extracts web data from Google Careers website through webdriver
    driver.get('https://careers.google.com/jobs/results/?distance=50&q=' + searchTerm)
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(id="search-results")
    return jobSoup
def extractJobTitleGoogle(jobElem): # extracts job title from web data
    print(jobElem)
    print("*****")
    titleElem = jobElem.find(class_="gc-card__title gc-heading gc-heading--beta")
    print(titleElem)
    title = titleElem.text.strip()
    return title
def extractJobLocationGoogle(jobElem): # extracts job location from web data
    locationElem = jobElem.find(class_="gc-job-tags__location")
    location = locationElem.text.strip()
    return location
def extractJobDateGoogle(jobElem): # extracts job date from web data
    dateElem = jobElem.find(itemprop="datePosted")
    date = dateElem.text.strip()
    return date
def extractJobLinkGoogle(jobElem): # extracts job link from web data
    link = "careers.google.com" + jobElem.find('a')['href']
    return link
def saveJobsToExcel(jobsList, filename): # update based on what format we want
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)
def findJobsFrom(website, searchTerm, desiredCharacs, filename="GoogleJobs.xlsx"): # loads Google website, extracts data and saves it
    if website == 'Google':
        jobSoup = loadGoogleJobs(searchTerm, driver)
        jobsList, numListings = extractJobInformationGoogle(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
        print('{} new job postings retrieved. Stored in {}.'.format(numListings, filename))
def extractJobInformationGoogle(jobSoup, desiredCharacs): # extracts data by searching for desired information per job
    jobElems = jobSoup.find_all('li')
    cols = []  # creates columns array
    extractedInfo = []  # creates array of info
    if 'titles' in desiredCharacs: # if titles in desired characs, creates title array
        titles = []
        cols.append('Titles')
        for jobElem in jobElems:
            titles.append(extractJobTitleGoogle(jobElem))
        extractedInfo.append(titles)
    if 'locations' in desiredCharacs: # if locations in desired characs, creates locations array
        locations = []
        cols.append('Locations')
        for jobElem in jobElems:
            locations.append(extractJobLocationGoogle(jobElem))
        extractedInfo.append(locations)
    if 'dates' in desiredCharacs: # if dates in desired characs, creates dates array
        dates = []
        cols.append('Dates')
        for jobElem in jobElems:
            dates.append(extractJobDateGoogle(jobElem))
        extractedInfo.append(dates)
    if 'links' in desiredCharacs: # if links in desired characs, creates links array
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractJobLinkGoogle(jobElem))
        extractedInfo.append(links)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j]
    numListings = len(extractedInfo[0])
    return jobsList, numListings
desiredCharacs = ['titles', 'locations', 'dates', 'links']
findJobsFrom('Google', 'data science intern', desiredCharacs)
