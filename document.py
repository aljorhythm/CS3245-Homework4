# Represents a document
class Document():
  def __init__(self, id, filepath):
    self.id = id
    self.filepath = filepath
  def getFilepath(self):
    return self.filepath
  def getId(self):
    return self.id