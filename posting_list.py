from term_weight import TermWeight
import math

# inverse document frequency
# returns inverse document frequency: log (N / df_t)
def inverse_document_frequency(number_of_documents, document_frequency):
  try:
    return math.log(number_of_documents / document_frequency, 10)
  except:
    return 0

# A single posting list
# Associated with a term and its frequencies in documents
class PostingList():
  def __init__(self, term):
    self.term = term
    self.term_frequencies = {}
  
  # get document frequency
  def getDocumentFrequency(self):
    return len(self.term_frequencies)
  
  # Get term associated with this posting list
  def getTerm(self):
    return self.term
  
  # increment term frequency in document
  def incrementTermFrequency(self, document_id):
    if not document_id in self.term_frequencies:
      self.term_frequencies[document_id] = TermWeight(document_id)
    self.term_frequencies[document_id].incrementFrequency()

  # returns inverse document frequency: log (N / df_t)
  def getInverseDocumentFrequency(self, number_of_documents):
    return inverse_document_frequency(number_of_documents, self.getDocumentFrequency())
  
  # returns a posting list of term weights of each document
  def getTermWeights(self):
    self.documentIds = self.term_frequencies.keys()
    sorted_document_ids = sorted(self.documentIds, key=lambda id: int(id))
    return [self.term_frequencies[document_id] for document_id in sorted_document_ids]
  
  # returns term weight for a document
  def getDocumentTermWeight(self, document_id):
    return self.term_frequencies[document_id] if document_id in self.term_frequencies else None
