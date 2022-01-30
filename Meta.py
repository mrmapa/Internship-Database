import requests
from bs4 import BeautifulSoup
import pandas as pd
def loadMetaJobs(searchTerm): # loads web data from Meta website given searchTerm
    url = ("https://www.facebookcareers.com/jobs/?q=" + searchTerm)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobSoup = soup.find(class_="_8tk7")
    print(jobSoup)
    return jobSoup
loadMetaJobs("summer intern")