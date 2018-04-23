
# Line reader
# Can read next int,int tuple in an already opened file
class LineReader():
  def __init__(self, file, start_position):
    self.file = file
    self.start_position = start_position
    self.current_position = self.start_position

  # read all ints on the line
  def allIntFloatTuples(self):
    store_position = self.current_position
    self.resetCursor()
    self.all_ints = self.nextIntFloatTuples()
    self.current_position = store_position
    return self.all_ints

  # reset cursor
  def resetCursor(self):
    self.current_position = self.start_position

  # get next integer on line, return None if end of line
  def nextIntFloatTuple(self):
    nextIntFloatTupleString = ""
    nextInt = ""
    
    while True:
      self.file.seek(self.current_position)
      nextChar = self.file.read(1)
      self.current_position += 1
      if nextChar is None or nextChar == '\n':
        self.current_position -= 1
        break
      elif nextChar == ' ':
        break
      else:
        nextIntFloatTupleString += nextChar
    
    if nextIntFloatTupleString == "":
      return None
    
    try:
      i, f = nextIntFloatTupleString.split("-")
      return (int(i), float(f))
    except:
      assert False, "not correct format"

  # gets all integers from cursor onwards
  def nextIntFloatTuples(self):
    IntFloatTuples = []
    while True:
      next = self.nextIntFloatTuple()
      if next == None:
        break
      IntFloatTuples.append(next)
    return IntFloatTuples