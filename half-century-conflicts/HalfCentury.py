# results class

class HalfCentury(object):
  """Represents a half centry of conflict data for a polity belligerent"""

  def __init__(self, politybelligerent, year):
    """initialize all internal properties"""
    # basic info
    self.politybelligerent = politybelligerent
    self.intStart = self.computeHalfCentury(year)
    self.intEnd = self.intStart + 49

    # tallies
    self.numConflicts = 0
    self.numCompletedConflicts = 0
    self.numVictories = 0
    self.numDraws = 0
    self.numLosses = 0
    self.yearsInConflict = set()
    self.conflictYears = 0

    # break-down tallies
    self.numNaval = 0
    self.yearsInNaval = set()
    self.navalYears = 0
    self.numSiege = 0
    self.yearsInSiege = set()
    self.siegeYears = 0
    self.numMajor = 0
    self.yearsInMajor = set()
    self.majorYears = 0

    # ratios
    self.winOverLoss = 0
    self.winOverTotal = 0

  def postProcessRow(self):
    """collapse sets used for counting"""
    self.yearsInConflict = len(self.yearsInConflict)
    self.yearsInNaval = len(self.yearsInNaval)
    self.yearsInSiege = len(self.yearsInSiege)
    self.yearsInMajor = len(self.yearsInMajor)
    if self.numLosses > 0:
      self.winOverLoss = self.numVictories / self.numLosses
    elif self.numVictories > 0:
      self.winOverLoss = 1
    if self.numCompletedConflicts > 0:
      self.winOverTotal = self.numVictories / self.numCompletedConflicts

  def getConflictRange(self, conflict_start, conflict_end):
    """get the set of conflict years in the current half century"""
    cropped_start = max(self.intStart, conflict_start)
    cropped_end = min(self.intStart+49, conflict_end)
    return set( range(cropped_start, cropped_end + 1) )

  def addYearsInConflict(self, conflict_range):
    """include unique years in conflict"""
    self.yearsInConflict = self.yearsInConflict.union(conflict_range)

  def updateNumConflicts(self):
    """increment the number of conflicts in the half century"""
    self.numConflicts += 1

  def updateConflictYears(self, conflict_len):
    """update the 'conflict years'"""
    self.conflictYears += conflict_len

  def updateNaval(self, conflict_range, conflict_len):
    """update naval properties"""
    self.numNaval += 1
    self.yearsInNaval = self.yearsInNaval.union(conflict_range)
    self.navalYears += conflict_len

  def updateMajor(self, conflict_range, conflict_len):
    """update major properties"""
    self.numMajor += 1
    self.yearsInMajor = self.yearsInMajor.union(conflict_range)
    self.majorYears += conflict_len

  def updateSiege(self, conflict_range, conflict_len):
    """update siege properties"""
    self.numSiege += 1
    self.yearsInSiege = self.yearsInSiege.union(conflict_range)
    self.siegeYears += conflict_len

  def updateVictories(self):
    self.numVictories += 1

  def updateDraws(self):
    self.numDraws += 1

  def updateLosses(self):
    self.numLosses += 1

  def updateCompleted(self):
    self.numCompletedConflicts += 1

  @staticmethod
  def computeHalfCentury(year):
    """get the half century that a year is in"""
    return year - (year % 50)

  @staticmethod
  def getHalfCenturyList(cstart, cend):
    """get every half century from cstart to cend inclusive"""
    half_start = HalfCentury.computeHalfCentury(cstart)
    return range(half_start, cend, 50)
