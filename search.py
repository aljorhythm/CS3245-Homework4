import os
import argparse
import time
from index import read_dictionary
from index import terms_from_content as terms_from_content_callback
from phrases_from_query import phrases_from_query
from file_reader import FileReader
from query import Query
import struct

try:
    import cPickle as pickle
except:
    import pickle

# returns array of queries
def read_query_file(filename):
  with open(filename) as file:
    lines = file.readlines()
    return (lines[0], lines[1:])

# returns search results of query (top 10)
def search(query_string, dictionary, posting_file_reader, query_to_phrases, terms_from_content, number_of_documents):
  query = Query(query_string, dictionary, posting_file_reader, query_to_phrases, terms_from_content, number_of_documents)
  results = query.getRankedDocumentScores()
  return results

# write results to file
def write_results(filename, results):
  with open(filename, 'wb') as file:
    results_str = "\n".join([" ".join([str(document_score["document_id"]) for document_score in result]) for result in results])
    file.writelines(results_str)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('-d', dest='dictionary_filename', help='no dictionary file')
  parser.add_argument('-p', dest='postings_filename', help='no postings file')
  parser.add_argument('-q', dest='query_filename', help='no queries file')
  parser.add_argument('-o', dest='results_filename', help='no results file')
  parser.add_argument('-t', dest='timed', action='store_true', help='time')
  args = parser.parse_args()
  args = vars(args)

  dictionary_filename = args["dictionary_filename"]
  query_filename = args["query_filename"]  
  postings_filename = args["postings_filename"]
  results_filename = args["results_filename"]
  timed = args["timed"]

  query, relevant_judgements = read_query_file(query_filename)
  dictionary = read_dictionary(dictionary_filename)
  terms = dictionary["terms"]
  number_of_documents = dictionary["meta"]["number_of_documents"]
  document_ids_to_index = dictionary["document_ids_to_index"]

  posting_file_reader = FileReader(postings_filename)

  start = time.time()

  search_results = []
  query = query.strip('\n')

  def terms_from_content(content):
    terms = []
    terms_from_content_callback(content, lambda term: terms.append(term))
    return terms

  search_result = search(query, terms, posting_file_reader, phrases_from_query, terms_from_content, document_ids_to_index)
  search_results.append(search_result)

  done = time.time()
  elapsed = done - start

  if timed:
    print "Started at {}, ended at {}, time taken: {}".format(start, done, elapsed)
  
  posting_file_reader.close()
  write_results(results_filename, search_results)