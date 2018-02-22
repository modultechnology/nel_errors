#!/usr/bin/python
 # -*- coding: utf8 -*-
'''
'''
import sys
import csv

print "start"

f = open(sys.argv[1], 'rt')
f2 = open(sys.argv[2], 'wb')
try:
    reader = csv.reader(f, delimiter="|")
    writer = csv.writer(f2, dialect=csv.excel_tab)
    for row in reader:
        print row
        writer.writerow(row)
finally:
    f.close()
    f2.close()
  
print "end"