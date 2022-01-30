from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe")
def loadBloombergJobs(searchTerm, driver): # extracts jobInfo from Bloomberg website through webdriver
    driver.get('https://careers.bloomberg.com/job/search?qf=' + searchTerm)
    """
    jobSearchBox = driver.find_element_by_id("search-text-input")
    jobSearchBox.send_keys(searchTerm)
    jobSearchBox.click()
    jobSearchBox.send_keys(Keys.ENTER)
    """
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(class_="job-results-list")
    return jobSoup
def extractJobTitleBloomberg(jobElem): # extracts job title from web data
    titleElem = jobElem.find(class_="job-results-name")
    title = titleElem.text.strip()
    return title
def extractJobLocationBloomberg(jobElem): # extracts job location from web data
    locationElem = jobElem.find(class_="job-results-city")
    location = locationElem.text.strip()
    return location
def extractJobDateBloomberg(jobElem): # extracts job date from web date
    dateElem = jobElem.find(class_="job-results-date")
    date = dateElem.text.strip()
    return date
def extractJobLinkBloomberg(jobElem): # extracts job link from web data
    link = "careers.bloomberg.com" + jobElem.find('a')['href']
    return link
def saveJobsToExcel(jobsList, filename): # update based on what format we want
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)
def findJobsFrom(website, searchTerm, desiredCharacs, filename="BloombergJobs.xlsx"): # loads Bloomberg website, extracts data and saves it
    if website == 'Bloomberg':
        jobSoup = loadBloombergJobs(searchTerm, driver)
        jobsList, numListings = extractJobInformationBloomberg(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
        print('{} new job postings retrieved. Stored in {}.'.format(numListings, filename))
def extractJobInformationBloomberg(jobSoup, desiredCharacs): # extracts data by searching for desired information per job
    jobElems = jobSoup.find_all(class_="job-results-section")
    cols = [] # creates columns array
    extractedInfo = [] # creates array of info
    company = []
    cols.append('Company')
    for jobElem in jobElems:
        company.append("Bloomberg")
    extractedInfo.append(company)
    if 'titles' in desiredCharacs: # if titles in desired characs, creates title array
        titles = []
        cols.append('Titles')
        for jobElem in jobElems:
            titles.append(extractJobTitleBloomberg(jobElem))
        extractedInfo.append(titles)
    if 'locations' in desiredCharacs: # if locations in desired characs, creates locations array
        locations = []
        cols.append('Locations')
        for jobElem in jobElems:
            locations.append(extractJobLocationBloomberg(jobElem))
        extractedInfo.append(locations)
    if 'dates' in desiredCharacs: # if dates in desired characs, creates dates array
        dates = []
        cols.append('Dates')
        for jobElem in jobElems:
            dates.append(extractJobDateBloomberg(jobElem))
        extractedInfo.append(dates)
    if 'links' in desiredCharacs: # if links in desired characs, creates links array
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractJobLinkBloomberg(jobElem))
        extractedInfo.append(links)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j]
    numListings = len(extractedInfo[0])
    return jobsList, numListings
desiredCharacs = ['titles', 'locations', 'dates', 'links']
findJobsFrom('Bloomberg', 'summer intern', desiredCharacs)