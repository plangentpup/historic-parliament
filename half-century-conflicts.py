#!/usr/bin/python
import mysql.connector


def getStartHalfCentury(year):
  return year - (year % 50)

def postProcessRow(row):
  row['yearsInConflict'] = len(row['yearsInConflict'])
  row['yearsInNaval'] = len(row['yearsInNaval'])
  row['yearsInSiege'] = len(row['yearsInSiege'])
  row['yearsInMajor'] = len(row['yearsInMajor'])
  return row

# connect to our database
cnx = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "root",
  db = "polity_conflict"
)

# define the cursor
cursor = cnx.cursor(dictionary=True)

# Use all the SQL you like
cursor.execute("SELECT DISTINCT * FROM conflicts ORDER BY politybelligerent, cstart")

# our output data
results = []
i = -1

# keep track of the last
for row in cursor:

  # get the half century from the conflict start year
  half_century = getStartHalfCentury(row['cstart'])

  if ( i < 0 or results[i]['politybelligerent'] != row['politybelligerent'] or results[i]['intStart'] != half_century):

    # run post processing on the last result row before creating the new one
    if i >= 0:
      results[i] = postProcessRow(results[i])

    # update the index
    i += 1

    # create the new (empty) result row
    results.append({
      'politybelligerent': row['politybelligerent'],
      'intStart': half_century,
      'intEnd': half_century + 49,
      'numConflicts': 0,
      'yearsInConflict': set(),
      'conflictYears': 0,
      'numNaval': 0,
      'yearsInNaval': set(),
      'navalYears': 0,
      'numSiege': 0,
      'yearsInSiege': set(),
      'siegeYears': 0,
      'numMajor': 0,
      'yearsInMajor': set(),
      'majorYears': 0
    })

  # get the set of conflict years from this row in the current half century
  conflict_start = max(half_century, row['cstart'])
  conflict_end = min(half_century+49, row['cend'])
  conflict_range = set(range(conflict_start, conflict_end + 1))
  conflict_len = len(conflict_range)

  # always incrememnt this
  results[i]['numConflicts'] += 1

  # add in the new years in conflict
  results[i]['yearsInConflict'] = results[i]['yearsInConflict'].union(conflict_range)

  # update the "conflict years"
  results[i]['conflictYears'] += conflict_len

  # update if it's a naval battle
  if row['navalbattle']:
    results[i]['numNaval'] += 1
    results[i]['yearsInNaval'] = results[i]['yearsInNaval'].union(conflict_range)
    results[i]['navalYears'] += conflict_len

  # update if it's a major battle
  if row['major']:
    results[i]['numMajor'] += 1
    results[i]['yearsInMajor'] = results[i]['yearsInMajor'].union(conflict_range)
    results[i]['majorYears'] += conflict_len

  # update if it's a siege
  if row['battletype'] == 'siege':
    results[i]['numSiege'] += 1
    results[i]['yearsInSiege'] = results[i]['yearsInSiege'].union(conflict_range)
    results[i]['siegeYears'] += conflict_len

# dont forget to run the averages on the last row!
results[i] = postProcessRow(results[i])
print results

# close the open connections
cursor.close()
cnx.close()