This is the README file for A0140036X's submission

== Python Version ==

I'm (We're) using Python Version <2.7.10> for
this assignment.

== General Notes about this assignment ==

Stemming, case-folding are done but punctuations are not removed

1. Indexing
  - Sentence are read from each file
  - File information is stored (document id)
  - Each sentence is tokenized into word tokens
  - Tokens are stemmed using porter stemmer to create terms
  - Terms are kept in a dictionary mapping of term to posting lists
  - Each term's frequency is incremented in the posting lists
  - For each term frequency in each document
    - frequency is logarthmically adjusted
    - every document's length is calculated (cosine normalized) summing these logarthmic frequencies as term weights
    - document length is recorded
    - every term weight (logarthmic frequency) is normalized against document length
  - After all the files are traversed
    - document ids are mapped to document indexes in vector space
    - written to dictionary file are
      - term information (term to line number and document frequency)
      - document lengths (normalized)
      - number of documents in total
      - document id to document index mapping
    - written to the posting file are
      - each line represents posting lists of a term
      - example: "2-1.3" represents document 2 with weight 1.3, which is the lnc 
      
  Key difference from Homework 3 is that term_from_token now takes a callback to reduce time complexity, ie. don't
  collect all the terms, return and then process. Instead right after stemming a token, the term is processed for
  indexing.

2. Searching
  - read information from dictionary file
  - extract query phrases from query
  - get query expansion from file if available
    - extract query terms from each query phrase
    - initialize empty document vectors
    - create query posting list (needed for ltc)
    - fill query posting list and document vectors
      - for each query term, get it's posting lists from posting list file
        - fill corresponding document vector element with term weights in posting lists
          - example: document id 1000 is at index 900, term weight is 2.3
          - document_vectors[900] = 2.3
        - increment term frequency in query posting list
    - fill query vector
      - for each query term
        - tf: calculate inverse document frequency (using total number of documents and document frequency)
        - idf: calculate logarthmic term frequency (using query posting list)
        - add tf * idf to query vector
    - calulate document scores
      - document vector and query vector and pairwise multipled and summed
  - scores from each phrase are intersected and summed
    - documents with scores of 0 are removed
  - all documents are sorted by scores
  - query expansion is performed
    - get top term which is alphanumeric and not in phrases
    - store it into file (query_expansions.json)

  gather all the results and print to output file

Tests
---------------------------------
Unit Tests are available on some scripts.
Running the script by default runs the test

1. file_reader.py - tests reading and seeking lines from file
2. query.py - contains quite extensive testing of boolean query operations using test_postings.txt
3. test_postings.txt - contains test postings for testing query algo
3. create_test_training.py - creates test training files according to week 7 slides

Also for printing purposes, the dictionary file can be printed in a readable format using
python print_dictionary.py dictionary.txt

Known Limitations or Bugs
---------------------------------
1. The file reader assumes that line number is always valid
2. The file reader also assumes that a line reader will not be requested
before
3. Sunfire does not have nltk, so no stemming is used if nltk is not detected
4. The seeking in line/file reader is rather naive, it might not take the shortest path

== Files included with this submission ==

document.py
- Represents a document object, used during indexing

file_reader.py
- a file reader object that seeks to line positions quickly without reading

index.py
- main indexing file
- contains tokenizer, term processing

line_reader.py
- a line reader to read to and fro a line of postings
- postings are "<document id>-<term weight>" delimited by spaces

phrases_from_query.py
- extracts phrases from query
- "A B C" and two -> ['A B C', 'and', 'two']

posting_list.py
- represents a posting list, used during indexing

print_dictionary.py
- utility method to print readable format from serialized dictionary file, can ignore

query.py
- abstract of free text query operations
- contains calls to query expansion

argparse.py
- because sunfire does not have argparse

search.py
- as specified by assignment

term_weight.py
- represents a term weight in document

write_csv_to_files.py
- writes contents in csv file to individual files for checking

Packages
----------------------------------
numpy, argparse, nltk

== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0140036X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==
