import requests
from furl import furl
from bs4 import BeautifulSoup

from jobdetails import JobDetails

class JobScraper:
    def __init__(self):
        self.job_processor = None # child class will instantiate

        # initialize all scrapers
        self.scrapers = []

        rg_scraper = RiotGamesJobScraper()
        bonfire_scraper = BonfireJobScraper()

        self.scrapers.append(rg_scraper)
        self.scrapers.append(bonfire_scraper)

    # get all the jobs from this particular instance of a scraper
    def getJobs(self):

        return self.job_processor()
    
    # pass in the response, return a bs4 representation of the page
    def getJobsPage(self, response):

        soup = None

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')     
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

        return soup
    
    # build the full url of a specific job listing
    def _buildURL(self, url):

        job_url_full = None

        host = furl(f'{self.base_url}').host
        scheme = furl(f'{self.base_url}').scheme

        if furl(url).path.isabsolute:
            job_url_full = scheme + "://" + host + url
        else: 
            job_url_full = self.base_url + url

        return job_url_full


#### --------------------------------------------------------------------------
class RiotGamesJobScraper(JobScraper):
    def __init__(self):
        self.base_url = "https://www.riotgames.com/en/work-with-us"
        self.response = requests.get(self.base_url)
        self.bs4 = self.getJobsPage(self.response)
        self.job_processor = self._getAllJobs

    # -------------------------------------
    # get all the jobs from the page
    # -------------------------------------
    def _getAllJobs(self):

        jobs = []

        job_elements = self.bs4.find_all(class_="job-row job-row--body")

        for job_element in job_elements:

            job_details = self._getJobDetails(job_element)
            jobs.append(job_details)

        return jobs

    # -------------------------------------
    # extract the details for a specific job
    # -------------------------------------
    def _getJobDetails(self, job_element):
            
        # Find the job URL -> (elements with class "js-job-url")
        job_parent_element = job_element.find("a", class_="js-job-url")
        job_url = job_parent_element.get("href")

        temp_contents = job_parent_element.contents

        # Find the job title -> (elements with class "job-row__col--primary")
        job_title = job_element.find(class_="job-row__col--primary").text

        # Find the job location 
        job_location = job_parent_element.contents[3].text

        return JobDetails(job_title, self._buildURL(job_url), job_location)
    
#### --------------------------------------------------------------------------
class BonfireJobScraper(JobScraper):
    def __init__(self):
        self.base_url = "https://www.bonfirestudios.com/careers"
        self.response = requests.get(self.base_url)
        self.bs4 = self.getJobsPage(self.response)
        self.job_processor = self._getAllJobs

    # -------------------------------------
    # get all the jobs from the page
    # -------------------------------------
    def _getAllJobs(self):

        jobs = []

        job_elements = self.bs4.find(id="openings").findChildren(class_="title subtitle")

        for job_element in job_elements:

            job_details = self._getJobDetails(job_element)
            jobs.append(job_details)

        return jobs

    # -------------------------------------
    # extract the details for a specific job
    # -------------------------------------
    def _getJobDetails(self, job_element):
            
        # Find the job URL
        job_parent_element = job_element.find("a")
        job_url = job_parent_element.get("href")

        # Find the job title -> (elements with class "job-row__col--primary")
        job_title = job_element.text.strip("\n\t")

        # Find the job location 
        job_location = "DEFAULT"

        return JobDetails(job_title, self._buildURL(job_url), job_location)