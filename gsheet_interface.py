import pygsheets # https://pygsheets.readthedocs.io/en/stable/index.html
import pandas as pd

class GSheetIO:
    def __init__(self):
        self.sheet_title = 'Tech Jobs - Database'

    def writeJobs(self, jobs):
        client = pygsheets.authorize() # https://pygsheets.readthedocs.io/en/stable/authorization.html

        # Open the spreadsheet and the first sheet.
        sh = client.open(self.sheet_title)
        wks = sh.sheet1

        #Get the data from the Sheet into python as DF
        jobs_df = wks.get_as_df()

        #Print the head of the datframe
        print(jobs_df)

        #In order to clear all the data in the sheet.
        wks.clear()

        jobs_list = []
        for job in jobs: # make a list to populate the dataframe
            jobs_list.append({ 'Job Title': job.title, 'Job Location': job.location,  'Job URL': job.url})

        # concat the two dataframes together (whatever was pulled from the gsheet plus new jobs)
        jobs_df = pd.concat([jobs_df, pd.DataFrame.from_records(jobs_list)])

        #We will use set_dataframe() in pygsheets to write df data into GS
        wks.set_dataframe(jobs_df,(1,1))    #(Row_Number, Column_Number)