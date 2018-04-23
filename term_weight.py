import math

#Represents a term weight in document
class TermWeight():
  def __init__(self, document_id):
    self.frequency = 0
    self.documentId = document_id
    self.fixed_weight = None

  # increments of frequency of term in document
  def incrementFrequency(self):
    self.frequency += 1

  # sets weight of term in document
  def setWeight(self, weight):
    self.fixed_weight = weight

  # gets weight of term in document
  # returns frequency if fixed weight not set
  def getWeight(self):
    return self.fixed_weight if self.fixed_weight is not None else self.getFrequency()

  # returns frequency of term in document
  def getFrequency(self):
    return self.frequency

  # returns logarithm term frequency
  def getLogarithmicFrequency(self):
    if self.frequency == 0:
      return 1
    else:
      return 1 + math.log(self.frequency, 10)

  # returns normalized logarithm term frequency
  # logarithmic frequency / document length
  def getNormalizedLogarithmicFrequency(self, document_length):
    return self.getLogarithmicFrequency() / document_length

  # returns tf_idf
  def getTfIdf(self, number_of_documents):
    return self.getLogarithmicFrequency() * self.getInverseDocumentFrequency(number_of_documents)

  # returns document id
  def getDocumentId(self):
    return self.documentId