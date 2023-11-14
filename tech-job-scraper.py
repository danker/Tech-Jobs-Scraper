from gsheet_interface import GSheetIO
from scrapers import jobscraper as js
    
# -------------------------------------
# MAIN
# -------------------------------------
scraper = js.JobScraper()

jobs = []

print(f"---STARTING---")

for s in scraper.scrapers: 
    jobs.extend(s.getJobs())

print(f"--DONE SCRAPING--")

print(f"--WRITING TO GSHEET--")
#gsio = GSheetIO()
#gsio.writeJobs(jobs)
   
for job in jobs:
    print(f"<-- {job.title} -->")
    print(f"LOCATION-> {job.location}")
    print(f"URL-> {job.url}")

print(f"--PROCESSED {len(jobs)} JOBS--")