import pygsheets # https://pygsheets.readthedocs.io/en/stable/index.html

client = pygsheets.authorize() # https://pygsheets.readthedocs.io/en/stable/authorization.html

# Open the spreadsheet and the first sheet.
sh = client.open('Tech Jobs - Database')
wks = sh.sheet1

# Update a single cell.
wks.update_value('A1', "FIRST")

wks.append_table([1, 2, 3], dimension='ROWS')
wks.append_table([2, 2, 3], dimension='ROWS')
wks.append_table([3, 2, 3], dimension='ROWS')

# Update the worksheet with the numpy array values. Beginning at cell 'A2'.
#wks.update_values('A2', my_numpy_array.to_list())

# Share the sheet with your friend. (read access only)
#sh.share('friend@gmail.com')
# sharing with write access
#sh.share('friend@gmail.com', role='writer')