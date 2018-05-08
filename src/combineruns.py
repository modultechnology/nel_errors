#!/usr/bin/python
 # -*- coding: utf8 -*-

'''
This script uses the combined run created simply by running sort -u file1 file2 file3 > combined-file.csv
Please use the following header:
doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|goldLink|S|B|A|R|
'''
import sys
import csv
import math

import pandas as pd

reload(sys)  
sys.setdefaultencoding('utf8')



print "start"
#REUTERS128
'''
df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters-spotlight.csv", delimiter="|")
df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters-babelnet.csv", delimiter="|")
df3 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters-aida.csv", delimiter="|")

df = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters-all.csv", delimiter="|") 
f2 = open("/home/adrian/git/error_analysis/tac/reuters50.csv", 'wb') 
'''

#KORE50
df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-spotlight.csv", delimiter="|")
df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-babelnet.csv", delimiter="|")
df3 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-aida.csv", delimiter="|")

df = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-all.csv", delimiter="|") 
f2 = open("/home/adrian/git/error_analysis/tac/kore50.csv", 'wb') 
#result = pd.DataFrame()


try:
    for index, row in df.iterrows():
        Spot = 0
        Babel = 0
        Ai = 0
        print row
        print row[0], row[1], row[2]
        
        #print df1[(df1['doc']==row[0])&(df1['start']==row[1])&(df1['end']==row[2])]
        #df33 = df1[(df1['doc']==row[0])&(df1['start']==row[1])&(df1['end']==row[2])&(df1['link']==row[3])]
        #print df33
        
        #'''
        dfsp = df1[(df1['doc']==row[0])&(df1['start']==row[1])&(df1['end']==row[2])&(df1['link']==row[3])]
        dfba = df2[(df2['doc']==row[0])&(df2['start']==row[1])&(df2['end']==row[2])&(df2['link']==row[3])]
        dfai = df3[(df3['doc']==row[0])&(df3['start']==row[1])&(df3['end']==row[2])&(df3['link']==row[3])]
        
        if not dfsp.empty:
            Spot = 1
        if not dfba.empty:
            Babel = 1
        if not dfai.empty:
            Ai = 1
        #'''
        
        docno = str(row[0])
        
        if docno!='AAA':
            start = str(row[1])
            end = str(row[2])
            link = str(row[3])
            type =  str(row[4])
            surfaceForm = str(row[5])
            tac = str(row[6])
                
            #inGold = str(row[9])
            #gold = str(row[10])
            
            if pd.isnull(row[10]):
                inGold = str(0)
                gold = ""
            else:
                inGold = str(1)
                gold = str(row[10])
            
            S = str(Spot)
            B = str(Babel)
            A = str(Ai)
            R = str(0)
            
            f2.write(docno)
            f2.write("|")
            f2.write(start)
            f2.write("|")
            f2.write(end)
            f2.write("|")
            f2.write(link)  
            f2.write("|")    
            f2.write(type)
            f2.write("|")
            f2.write(surfaceForm)
            f2.write("|")
            f2.write(tac)  
            f2.write("|")
            f2.write("")  
            f2.write("|")
            f2.write("")  
            f2.write("|")
            f2.write(inGold)
            f2.write("|")
            f2.write(gold)
            f2.write("|")
            f2.write(S)  
            f2.write("|")    
            f2.write(B)
            f2.write("|")
            f2.write(A)
            f2.write("|")
            f2.write(R)  
            f2.write("|")
            #f2.write(score)
            #f2.write("|")
            f2.write("\n")     
finally:
        f2.close()






#result.to_csv(f2, sep='|', float_format='%.f', encoding='utf-8')

print "end"
'''
if __name__ == '__main__':
    print "start"

    combine()
    
    print "end"
'''