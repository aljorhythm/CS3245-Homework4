# write data from csv to files

import csv
import sys
import os

csv.field_size_limit(sys.maxsize)

training_file = "~/Downloads/dataset/dataset.csv"
training_file = os.path.expanduser(training_file)

with open(training_file) as csvfile:
  csvreader = csv.reader(csvfile)

  row_number = 1
  for row in csvreader:

    # heading
    if row_number == 1:
      row_number += 1
      continue

    row_number += 1

    document_id = row[0].decode('utf-8')
    content = row[2].decode('utf-8')

    filename = "data/{}".format(document_id)
    with open(filename, 'w') as file:
        file.write(content.encode('utf-8'))