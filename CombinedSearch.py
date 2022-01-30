from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
options = Options()
# Performing without GUI
options.headless = True
options.add_argument("--window-size=1920,1200")
# Accepting downloads without GUI
options.add_experimental_option("prefs", {
  "download.default_directory": r"/Users/marcosantos/Downloads",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing_for_trusted_sources_enabled": False,
  "safebrowsing.enabled": False
})
driver = webdriver.Chrome(r"C:\Users\mrmap\PycharmProjects\Internship-Database\chromedriver.exe", options=options)

########## Accenture-Specific Functions ##########

def loadAccentureJobs(searchTerm, driver): # extracts jobInfo from Accenture website through webdriver
    try:
        driver.get("https://www.accenture.com/us-en/careers/jobsearch?jk=" + searchTerm)
        driver.implicitly_wait(10)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")
        jobSoup = soup.find(class_="upper-set-jobs job-listing-block col-xs-12")
        return jobSoup
    except AttributeError as err:
        print("Attribute Error: ".format(err))

def extractJobTitleAccenture(jobElem): # extracts job title from web data
    try:
        titleElem = jobElem.find('h3', class_="job-title module-title corporate-bold")
        title = titleElem.text.strip()
        return title
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobLocationAccenture(jobElem): # extracts job location from web data
    try:
        locationElem = jobElem.find('p', class_="small ucase job-location")
        location = locationElem.text.strip()
        return location
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobDateAccenture(jobElem): # extracts job posting date from web data
    try:
        dateElem = jobElem.find('p', class_="posted-date small acn-italic")
        date = dateElem.text.strip()
        return date
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobLinkAccenture(jobElem): # extracts link from web data
    try:
        link = jobElem.find('a')['href']
        return link
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobInformationAccenture(jobSoup, desiredCharacs): # extracts data by searching for desired information per job
    jobElems = jobSoup.find_all(class_="module job-card-wrapper col-md-4 col-xs-12 col-sm-6 corporate-regular background-white")
    cols = [] # creates array of columns
    extractedInfo = [] # creates array of info
    company = []
    cols.append('Company')
    for jobElem in jobElems:
        company.append("Accenture")
    extractedInfo.append(company)
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
    return jobsList

########## Bloomberg-Specific Functions ##########

def loadBloombergJobs(searchTerm, driver): # extracts jobInfo from Bloomberg website through webdriver
    driver.get('https://careers.bloomberg.com/job/search?qf=' + searchTerm)
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(class_="job-results-list")
    return jobSoup

def extractJobTitleBloomberg(jobElem): # extracts job title from web data
    try:
        titleElem = jobElem.find(class_="job-results-name")
        title = titleElem.text.strip()
        return title
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobLocationBloomberg(jobElem): # extracts job location from web data
    try:
        locationElem = jobElem.find(class_="job-results-city")
        location = locationElem.text.strip()
        return location
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobDateBloomberg(jobElem): # extracts job date from web date
    try:
        dateElem = jobElem.find(class_="job-results-date")
        date = dateElem.text.strip()
        return date
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobLinkBloomberg(jobElem): # extracts job link from web data
    try:
        link = "careers.bloomberg.com" + jobElem.find('a')['href']
        return link
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

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
    return jobsList

########## L3Harris-Specific Functions ##########

def loadL3HarrisJobs(searchTerm): # loads web data from L3Harris website given searchTerm
    url = ("https://careers.l3harris.com/search-jobs/" + searchTerm + "/")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobSoup = soup.find('section', id="search-results-list")
    return jobSoup

def extractTitleL3Harris(jobElem): # extracts job title from each job element
    try:
        titleElem = jobElem.find('h2')
        title = titleElem.text.strip()
        return title
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractLocationL3Harris(jobElem): # extracts job location from each job element
    try:
        locationElem = jobElem.find('span', class_="results-facet job-location")
        location = locationElem.text.strip()
        return location
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractLinkL3Harris(jobElem): # extracts job link from each job element
    try:
        link = jobElem.find('a')['href']
        link = "https://careers.l3harris.com/" + link
        return link
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractDateL3Harris(jobElem): # extracts job date from each job element
    try:
        dateElem = jobElem.find('span', class_="results-facet job-date-posted")
        date = dateElem.text.strip()
        return date
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

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
    if 'dates' in desiredCharacs: # creates Dates column and appends to extractedInfo
        dates = []
        cols.append('Date Listed')
        for jobElem in jobElems:
            dates.append(extractDateL3Harris(jobElem))
        extractedInfo.append(dates)
    if 'links' in desiredCharacs: # creates Links column and appends to extractedInfo
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append(extractLinkL3Harris(jobElem))
        extractedInfo.append(links)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j] # copies extractedInfo to jobsList so it can be returned
    return jobsList

########## Meta-Specific Functions ##########

def loadMetaJobs(searchTerm, driver): # extracts jobInfo from Meta website through webdriver
    driver.get("https://www.facebookcareers.com/jobs/?q=" + searchTerm)
    driver.implicitly_wait(10)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, "html.parser")
    jobSoup = soup.find(class_="_8tk7")
    return jobSoup

def extractJobTitleMeta(jobElem): # extracts job title from web data
    try:
        titleElem = jobElem.find(class_="_8sel _97fe")
        title = titleElem.text.strip()
        return title
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

def extractJobLocationMeta(jobElem): # extracts job location from web data
    try:
        locationElem = jobElem.find(class_="_8see _97fe")
        location = locationElem.text.strip()
        return location
    except AttributeError as err:
        print("Attribute Error: ".format(err))
        return "N/A"

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
    if 'dates' in desiredCharacs: # if dates in desired characs, fills with N/A
        dates = []
        cols.append('Dates')
        for jobElem in jobElems:
            dates.append("N/A")
        extractedInfo.append(dates)
    if 'links' in desiredCharacs:  # if links in desired characs, fills links with N/A
        links = []
        cols.append('Links')
        for jobElem in jobElems:
            links.append("N/A")
        extractedInfo.append(links)
    jobsList = {}
    for j in range(len(cols)):
        jobsList[cols[j]] = extractedInfo[j]
    return jobsList

########## SaveJobsToExcelFunction - useful for testing ##########

def saveJobsToExcel(jobsList, filename): # update based on what format we want
    jobs = pd.DataFrame(jobsList)
    jobs.to_excel(filename)

def findJobsFrom(website, searchTerm, desiredCharacs, filename="Internships.xlsx"): # extracts data by searching for desired information per job
    if website == 'Accenture': # exclusively Accenture positions
        jobSoup = loadAccentureJobs(searchTerm, driver)
        jobsList = extractJobInformationAccenture(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
    if website == 'Bloomberg': # exclusively Bloomberg positions
        jobSoup = loadBloombergJobs(searchTerm, driver)
        jobsList = extractJobInformationBloomberg(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
    if website == 'L3Harris': # exclusively L3Harris positions
        jobSoup = loadL3HarrisJobs(searchTerm)
        jobsList = extractJobInformationL3Harris(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
    if website == 'Meta': # exclusively Meta positions
        jobSoup = loadMetaJobs(searchTerm, driver)
        jobsList = extractJobInformationMeta(jobSoup, desiredCharacs)
        saveJobsToExcel(jobsList, filename)
    else: # combined table with every company
        # Step 1: retrieve data for each
        jobSoupAccenture = loadAccentureJobs(searchTerm, driver)
        jobSoupBloomberg = loadBloombergJobs(searchTerm, driver)
        jobSoupL3 = loadL3HarrisJobs(searchTerm)
        jobSoupMeta = loadMetaJobs(searchTerm, driver)

        # Step 2: convert to jobsList
        jobsListAccenture = extractJobInformationAccenture(jobSoupAccenture, desiredCharacs)
        jobsListBloomberg = extractJobInformationBloomberg(jobSoupBloomberg, desiredCharacs)
        jobsListL3 = extractJobInformationL3Harris(jobSoupL3, desiredCharacs)
        jobsListMeta = extractJobInformationMeta(jobSoupMeta, desiredCharacs)

        # Step 3: jobsList to DataFrame
        jobsFrameAccenture = pd.DataFrame(jobsListAccenture)
        jobsFrameBloomberg = pd.DataFrame(jobsListBloomberg)
        jobsFrameL3 = pd.DataFrame(jobsListL3)
        jobsFrameMeta = pd.DataFrame(jobsListMeta)

        # Step 4: concat each DataFrame together
        combinedJobs = pd.concat([jobsFrameAccenture, jobsFrameBloomberg])
        combinedJobs = pd.concat([combinedJobs, jobsFrameL3])
        combinedJobs = pd.concat([combinedJobs, jobsFrameMeta])
        combinedJobs.to_excel(filename)

desiredCharacs = ['titles', 'locations', 'dates', 'links']
findJobsFrom('All', "banana", desiredCharacs)