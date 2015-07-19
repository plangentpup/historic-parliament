#!/usr/bin/python
import mysql.connector

# import the database settings
import settings

# import the results class
from HalfCentury import HalfCentury

# import helper functions
import helper



# connect to our database
cnx = mysql.connector.connect(
  host   = settings.db["host"],
  user   = settings.db["user"],
  passwd = settings.db["passwd"],
  db     = settings.db["db"]
)

# define the cursor
cursor = cnx.cursor(dictionary=True)

# Use all the SQL you like
cursor.execute("SELECT DISTINCT * FROM conflicts ORDER BY politybelligerent, cstart")

# our output data. each element in the list is a HalfCentury object
results = []

# iterate over each conflict
for row in cursor:

  # get every half century from cstart to cend inclusive
  half_century_list = HalfCentury.getHalfCenturyList(cstart=row['cstart'], cend=row['cend'])

  for half_century in half_century_list:
    # see if this half century already exists
    halfCentury = helper.findHalfCentury(results, row['politybelligerent'], half_century)

    if halfCentury == False:
      # create a new half century if we haven't already
      halfCentury = HalfCentury(politybelligerent=row['politybelligerent'], year=half_century)
      results.append(halfCentury)

    # update the half century with data from the conflict
    helper.updateHalfCentury(halfCentury, row)

# now that the tallies are complete, run the post processing
for result in results:
  result.postProcessRow()

# close the open connections
cursor.close()
cnx.close()

# print the results
print [result.__dict__ for result in results]
