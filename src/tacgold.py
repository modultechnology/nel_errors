#!/usr/bin/python
 # -*- coding: utf8 -*-
'''
'''
import sys
import csv

print "start"
reload(sys)  
sys.setdefaultencoding('utf8')

def extract_url(text):      
  import re
  right_url = ''
  matches=re.findall(r'\"(.+?)\"',text)
  # matches is now ['String 1', 'String 2', 'String3']
  if matches:
      right_url = matches[0]
  return right_url


f = open(sys.argv[1], 'rt')
f2 = open(sys.argv[2], 'wb') 

try:
    reader = csv.reader(f, dialect=csv.excel_tab)
    writer = csv.writer(f2, delimiter="|")
    for row in reader:
        #print row
        f2.write(row[0])
        f2.write("|")
        f2.write(row[1])
        f2.write("|")
        f2.write(row[2])
        f2.write("|")
        
        f2.write(row[3])
        f2.write("|")
        f2.write(row[4])  
        f2.write("|")
        f2.write(row[5])  
        f2.write("|")
        f2.write("\n")     
      
        #writer.writerow(row)
finally:
    f.close()
    f2.close()



#print doit('Regex should return "String 1" or "String 2" or "String3" ')
#print extract_url('s"http://de.dbpedia.org/resource/Ukrainische_Sozialistische_Sowjetrepublik"')
# result:
#'String 1,String 2,String3'

print "end"