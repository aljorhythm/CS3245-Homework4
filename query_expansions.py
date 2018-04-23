# retrieve and add query expansions

import os
import json

filename = 'query_expansions.json'

# returns None if does not exist
def get_query_expansion(query_phrases):
  query_phrases = ",".join(query_phrases)
  expansions = get_query_expansions()
  if query_phrases in expansions:
    return expansions[query_phrases].split(",")
  else:
    return None

# get all query expansions
def get_query_expansions():
  try:
    return json.load(open(filename))
  except:
    return {}
  
# adds term to query phrases and stores expansions
def add_query_expansion(query_phrases, term):
  extended_query_phrases = ",".join(query_phrases + ['and', term])
  query_phrases = ",".join(query_phrases)
  expansions = get_query_expansions()
  expansions[query_phrases] = extended_query_phrases
  with open(filename, 'w') as outfile:
    json.dump(expansions, outfile)