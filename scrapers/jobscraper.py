import requests
from furl import furl
from bs4 import BeautifulSoup

from jobdetails import JobDetails

class JobScraper:
    def __init__(self):
        # initialize all scrapers
        self.scrapers = []

        rgScraper = RiotGamesJobScraper()

        self.scrapers.append(rgScraper)

    def getJobs(self):

        jobs = []

        for job_element in self.job_elements:

            job_details = self.getJobDetails(job_element)
            jobs.append(job_details)

        return jobs

class RiotGamesJobScraper(JobScraper):
    def __init__(self):
        self.base_url = "https://www.riotgames.com/en/work-with-us"
        self.response = requests.get(self.base_url)
        self.job_elements = ""

        # Check if the request was successful (status code 200)
        if self.response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(self.response.text, 'html.parser')

            # Find elements with class "job-row job-row--body"
            self.job_elements = soup.find_all(class_="job-row job-row--body")       
        else:
            print(f"Failed to retrieve the page. Status code: {self.response.status_code}")

    # -------------------------------------
    # extract the details for a specific job
    # -------------------------------------
    def getJobDetails(self, job_element):
            
        # Find the job URL -> (elements with class "js-job-url")
        job_parent_element = job_element.find("a", class_="js-job-url")
        job_url = job_parent_element.get("href")

        temp_contents = job_parent_element.contents

        # Find the job title -> (elements with class "job-row__col--primary")
        job_title = job_element.find(class_="job-row__col--primary").text

        # Find the job location 
        job_location = job_parent_element.contents[3].text

        # full URL
        job_url_full = ""
        host = furl(f'{self.base_url}').host
        scheme = furl(f'{self.base_url}').scheme
        if furl(job_url).path.isabsolute:
            job_url_full = scheme + "://" + host + job_url
        else: 
            job_url_full = self.base_url + job_url

        return JobDetails(job_title, job_url_full, job_location)