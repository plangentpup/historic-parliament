
def findHalfCentury(list, name, start_year):
  # search list for a half century that matchs name and start year
  for item in list:
    if (item.politybelligerent == name and item.intStart == start_year):
      return item

  # if we dont find it, return False
  return False

def updateHalfCentury(halfCentury, row):
  # get the set of conflict years from this row in the current half century
  conflict_range = halfCentury.getConflictRange(conflict_start=row['cstart'], conflict_end=row['cend'])
  conflict_len = len(conflict_range)

  # always incrememnt this
  halfCentury.updateNumConflicts()

  # add in the new years in conflict
  halfCentury.addYearsInConflict(conflict_range=conflict_range)

  # update the "conflict years"
  halfCentury.updateConflictYears(conflict_len=conflict_len)

  # update if it's a naval battle
  if row['navalbattle']:
    halfCentury.updateNaval(conflict_range=conflict_range, conflict_len=conflict_len)

  # update if it's a major battle
  if row['major']:
    halfCentury.updateMajor(conflict_range=conflict_range, conflict_len=conflict_len)

  # update if it's a siege
  if row['battletype'] == 'siege':
    halfCentury.updateSiege(conflict_range=conflict_range, conflict_len=conflict_len)

  # if the conflict ends this half century
  if halfCentury.intStart == halfCentury.computeHalfCentury(year=row['cend']):

    # update the completed conflicts tally
    halfCentury.updateCompleted()

    # update if it's a victory
    if row['belligerentvictor']:
      halfCentury.updateVictories()
    elif row['battledraw']:
      halfCentury.updateDraws()
    else:
      halfCentury.updateLosses()