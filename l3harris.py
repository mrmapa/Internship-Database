import requests
from bs4 import BeautifulSoup
import pandas as pd
def loadL3HarrisJobs(searchTerm): # loads web data from L3Harris website given searchTerm
    url = ("https://careers.l3harris.com/search-jobs/" + searchTerm + "/")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobSoup = soup.find('section', id="search-results-list")
    return jobSoup
def extractTitleL3Harris(jobElem): # extracts job title from each job element
    titleElem = jobElem.find('h2')
    title = titleElem.text.strip()
    return title
def extractLocationL3Harris(jobElem): # extracts job location from each job element
    locationElem = jobElem.find('span', class_="results-facet job-location")
    location = locationElem.text.strip()
    return location
def extractLinkL3Harris(jobElem): # extracts job link from each job element
    link = jobElem.find('a')['href']
    link = "https://careers.l3harris.com/" + link
    return link
def extractDateL3Harris(jobElem): # extracts job date from each job element
    dateElem = jobElem.find('span', class_="results-facet job-date-posted")
    date = dateElem.text.strip()
    return date
def saveJobsToExcel(jobsList, filename): # saves job data to excel spreadsheet
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)
def findJobsFrom(website, searchTerm, desiredCharacs, filename="test.xlsx"): # finds jobs given website, searchterm, desiredCharacs, and filename
    if website == 'L3Harris':
        jobSoup = loadL3HarrisJobs(searchTerm)
        jobsList = extractJobInformationL3Harris(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
def extractJobInformationL3Harris(jobSoup, desiredCharacs): # extracts jobInfo from the L3Harris website
    jobElems = jobSoup.find_all('li')
    cols = []
    extractedInfo = []
    company = []
    cols.append('Company')
    for jobElem in jobElems:
        company.append("L3Harris")
    extractedInfo.append(company)
    if 'titles' in desiredCharacs: # creates Titles column and appends to extractedInfo
        titles = []
        cols.append('Titles')
        for jobElem in jobElems:
            titles.append(extractTitleL3Harris(jobElem))
        extractedInfo.append(titles)
    if 'locations' in desiredCharacs: # creates Locations column and appends to extractedInfo
        locations = []
        cols.append('Locations')
        for jobElem in jobElems:
            locations.append(extractLocationL3Harris(jobElem))
        extractedInfo.append(locations)
    if 'links' in desiredCharacs: # creates Links column and appends to extractedInfo
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractLinkL3Harris(jobElem))
        extractedInfo.append(links)
    if 'dates' in desiredCharacs: # creates Dates column and appends to extractedInfo
        dates = []
        cols.append('Date Listed')
        for jobElem in jobElems:
            dates.append(extractDateL3Harris(jobElem))
        extractedInfo.append(dates)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j] # copies extractedInfo to jobsList so it can be returned
    return jobsList
    print('{} new job postings retrieved. Stored in {}.'.format(filename))
desiredCharacs = ['titles', 'locations', 'links', 'dates']
findJobsFrom('L3Harris', 'intern', desiredCharacs)