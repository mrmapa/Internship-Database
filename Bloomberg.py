import requests
from bs4 import BeautifulSoup
import pandas as pd
def loadBloombergJobs(searchTerm): # loads web data from Bloomberg website given searchTerm
    url = ("https://careers.bloomberg.com/job/search?qf=" + searchTerm)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobSoup = soup.find(class_="job-results-list")
    print(jobSoup)
    return jobSoup
loadBloombergJobs("summer intern")