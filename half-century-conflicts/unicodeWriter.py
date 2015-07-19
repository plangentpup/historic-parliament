import csv, codecs, cStringIO

class UnicodeWriter:
  """
  A CSV writer which will write rows to CSV file "f",
  which is encoded in the given encoding.
  @see https://docs.python.org/2.7/library/csv.html#csv-examples
  """

  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    # Redirect output to a queue
    self.queue = cStringIO.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.stream = f
    self.encoder = codecs.getincrementalencoder(encoding)()

  def writerow(self, row):
    encoded = []
    for s in row:
      if isinstance( s, int ):
        s = str(s)
      encoded.append(s.encode("utf-8"))

    #self.writer.writerow([s.encode("utf-8") for s in row])
    self.writer.writerow(encoded)

    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode("utf-8")

    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)

    # write to the target stream
    self.stream.write(data)

    # empty queue
    self.queue.truncate(0)

  def writerows(self, rows):
    for row in rows:
      self.writerow(row)