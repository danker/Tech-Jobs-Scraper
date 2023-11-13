import pygsheets # https://pygsheets.readthedocs.io/en/stable/index.html
import pandas as pd

client = pygsheets.authorize() # https://pygsheets.readthedocs.io/en/stable/authorization.html

# Open the spreadsheet and the first sheet.
sh = client.open('Tech Jobs - Database')
wks = sh.sheet1

#Get the data from the Sheet into python as DF
jobs_df = wks.get_as_df()

#Print the head of the datframe
print(jobs_df)

#In order to clear all the data in the sheet.
wks.clear()

jobs_df = pd.concat([jobs_df, pd.DataFrame.from_records(
    [{ 'Job Title': 'X1', 'Job Location': 'XJL',  'Job URL': 'XJU'}])])

#We will use set_dataframe() in pygsheets to write df data into GS
wks.set_dataframe(jobs_df,(1,1))    #(Row_Number, Column_Number)

# Write a few rows
#wks.append_table(data, dimension='ROWS', overwrite=True)


# Update the worksheet with the numpy array values. Beginning at cell 'A2'.
#wks.update_values('A2', my_numpy_array.to_list())

# Share the sheet with your friend. (read access only)
#sh.share('friend@gmail.com')
# sharing with write access
#sh.share('friend@gmail.com', role='writer')