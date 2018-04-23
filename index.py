# indexing script

import math
import argparse
import os
import csv
import sys

from itertools import chain
from posting_list import PostingList
from document import Document

try:
    import cPickle as pickle
except:
    import pickle
import struct

# csv file might be big
csv.field_size_limit(sys.maxsize)

try:
  from nltk.stem import PorterStemmer
  from nltk.tokenize import sent_tokenize, word_tokenize
  ps = PorterStemmer()
  # transform term into token
  def term_from_token(token, on_each_term):
    after = ps.stem(token.lower())
    on_each_term(after)
except:
  # transform term into token
  def term_from_token(token, on_each_term):
    on_each_term(after)

  # sent_tokenize
  def sent_tokenize(sentences):
    return sentences.split(".")

  # word_tokenize
  def word_tokenize(sentence):
    return sentence.split(" ")

# Term that will return all documents
global_term = ''

# (w1 ^ 2 + w2 ^ 2 + ... + wN ^ 2) ^ 1/2
def square_root_of_summation_of_squares(ws):
  try:
    return pow(sum([pow(w, 2) for w in ws]), 0.5)
  except:
    return 0

# transform tokens into terms
def terms_from_tokens(tokens, on_each_term):
  for token in tokens:
    term_from_token(token, on_each_term)

# get terms from content
# operations are sentence tokenizing, word tokenizing, case folding then stem
# encode with utf-8
def terms_from_content(content, on_each_term):
  for sentence in sent_tokenize(content):
    for tokens in word_tokenize(sentence):
      terms = terms_from_tokens(tokens, on_each_term)

# writes postings lists to file
def write_posting_lists(filename, indexer):
  posting_lists = indexer.sorted_posting_lists
  document_lengths = indexer.document_lengths
  # by writing string
  with open(filename, 'w') as file:
    lines = [" ".join(["{0}-{1}".format(term_weight.getDocumentId(), term_weight.getNormalizedLogarithmicFrequency(document_lengths[term_weight.getDocumentId()])) for term_weight in posting_list.getTermWeights()]) + "\n" for posting_list in posting_lists]
    file.writelines(lines)

# accepts a sorted array of posting lists, see sorted_array_posting_list()
# write terms and other information to dictionary
def write_dictionary(filename, indexer):
  posting_lists = indexer.sorted_posting_lists
  number_of_documents = indexer.number_of_documents
  meta = { "number_of_documents": number_of_documents }
  terms = [(posting_list.getTerm(), posting_list.getDocumentFrequency()) for posting_list in posting_lists]
  document_lengths = indexer.document_lengths
  document_ids = sorted(document_lengths.keys(), key=lambda id_string: int(id_string))
  document_ids_to_index = {}
  for index, document_id in enumerate(document_ids):
    document_ids_to_index[document_id] = index

  with open(filename, 'w') as file:
    data = {
      "meta" : meta,
      "terms" : dictionary_list_to_dict(terms),
      "document_lengths" : document_lengths,
      "document_ids_to_index" : document_ids_to_index
    }
    serialized = pickle.dumps(data)
    file.write(serialized)

# accepts a sorted array of dictionary term information, see sorted_array_posting_list()
# returns a sorted array of dictionary term information
def read_dictionary(filename):
  with open(filename, 'r') as file:
    serialized = file.read()
    return pickle.loads(serialized)

# used in write_dictionary() to convert terms information into dictionary
def dictionary_list_to_dict(dictionary_list):
  dict_representation = {}
  for index, term in enumerate(dictionary_list):
    dict_representation[term[0]] = { "line_number" : index + 1, "posting_counts" : term[1] }
  return dict_representation

# Represents construction of the dictionary and posting list
# lnc scheme is used for posting lists
class Indexer():
  def __init__(self, dataset_file, documents_limit=None):
    self.number_of_documents = 0
    self.posting_lists, self.document_lengths = self.retrieve_posting_lists_and_document_lengths(dataset_file, documents_limit)
    self.sorted_posting_lists = self.sorted_array_posting_list(self.posting_lists)

  # returns dict of vocabulary and corresponding posting list
  # can introduce a limit to the number of documents
  # counts the number of documents, if limit exists it will be used as number of documents
  # posting list
  def retrieve_posting_lists_and_document_lengths(self, training_file, documents_limit=None):
    
    posting_lists = {}
    documents = {}

    with open(training_file) as csvfile:
      csvreader = csv.reader(csvfile)

      row_number = 1
      for row in csvreader:
        print row_number

        # heading
        if row_number == 1:
          row_number += 1
          continue

        if documents_limit is not None and row_number > documents_limit:
          break
        row_number += 1

        document_id = row[0].decode('utf-8')
        content = row[2].decode('utf-8')

        def on_each_term(term):
          documents[document_id] = {}

          # increment term posting list
          if not term in posting_lists:
            posting_lists[term] = PostingList(term)

          posting_lists[term].incrementTermFrequency(document_id)

          documents[document_id][term] = posting_lists[term]

        # get terms from document
        terms = terms_from_content(content, on_each_term)
          
    document_lengths = {}

    for document_id, document_posting_lists in documents.items():

      # count terms in document
      document_term_counts = []

      # logarthmic counting
      for term, posting_list in document_posting_lists.items():
        document_term_counts.append(posting_list.getDocumentTermWeight(document_id).getLogarithmicFrequency())
      
      # normalized document length
      document_lengths[document_id] = square_root_of_summation_of_squares(document_term_counts)

    self.number_of_documents = row_number

    return (posting_lists, document_lengths)

  # accepts a dictionary of posting lists
  # returns a sorted array of posting lists which is consistent in dictionary and posting list file
  def sorted_array_posting_list(self, posting_lists):
    return [posting_lists[key] for key in sorted(posting_lists.keys())]

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Indexing')
  parser.add_argument('-i', dest='dataset_file', help='no directory')
  parser.add_argument('-d', dest='dictionary_file', help='no dictionary file')
  parser.add_argument('-p', dest='postings_file', help='no postings file')
  parser.add_argument('-l', dest='documents_limit', nargs='?', type=int, default=None, help='documents limit, used for testing/ trials')
  args = parser.parse_args()
  args = vars(args)

  dictionary_file = args["dictionary_file"]
  dataset_file = args["dataset_file"]
  postings_file = args["postings_file"]
  documents_limit = args["documents_limit"]

  indexer = Indexer(dataset_file, documents_limit)

  write_posting_lists(postings_file, indexer)
  write_dictionary(dictionary_file, indexer)