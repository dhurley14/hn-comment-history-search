"""
Upload the data stored in temp_output.txt into elasticsearch
"""

import cPickle as pickle
import elasticsearch

ITEMS = []
ES = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
with open('temp_output.txt', 'rb') as readFile:
    while 1:
        try:
            ITEMS.append(pickle.load(readFile))
            print ITEMS
            print len(ITEMS)
        except EOFError:
            break # no more data in the file.

MY_INDEX = 0
for item in ITEMS:
    for obj in item:
        print MY_INDEX
        ES.index(index='saved_comments', doc_type='comment', id=MY_INDEX, body=obj)
        MY_INDEX += 1
