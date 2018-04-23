# Prints dictionary

from index import read_dictionary
import sys

dictionary_file = sys.argv[1] if len(sys.argv) > 1 else "dictionary.txt"
dictionary = read_dictionary(dictionary_file)

print dictionary['document_ids_to_index']
print "{0}:\t\t{1}\t{2}".format("term", "line_number", "posting_counts")

terms = dictionary["terms"]
for term, term_info in terms.items():
  term = term
  line_number = term_info["line_number"]
  posting_counts = term_info["posting_counts"]
  print "{0}".format(term.encode('utf-8'))

print "Number of documents: {0}".format(dictionary["meta"]["number_of_documents"])

# print dictionary["document_ids_to_index"]