#!/usr/bin/python
 # -*- coding: utf8 -*-

'''
This script creates unified tac-toolOutput file ready for merging.
Please note that the values for |S|B|A|R| will be 0 after running this script 
Please use the following header:
doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|goldLink|S|B|A|R|
'''
import sys
import csv
import math

import pandas as pd

reload(sys)  
sys.setdefaultencoding('utf8')

#
#f = open(sys.argv[1], 'rt')
#N3-REUTERS128
#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-spotlight-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-spotlight-surface.csv", delimiter="|")


#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-babelnet-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-babelnet-surface.csv", delimiter="|")


#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-aida-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/reuters128-aida-surface.csv", delimiter="|")

#KORE50
#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-spotlight-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-spotlight-surface.csv", delimiter="|")


#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-babelnet-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-babelnet-surface.csv", delimiter="|")


#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-aida-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/kore50-aida-surface.csv", delimiter="|")

#RBB150
#df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/rbb-spotlight-fp.csv", delimiter="|")
#df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/rbbrun-surface.csv", delimiter="|")


df1 = pd.read_csv("/home/adrian/git/error_analysis/tac/rbb-recognyze-fp.csv", delimiter="|")
df2 = pd.read_csv("/home/adrian/git/error_analysis/tac/rbbrun-surface.csv", delimiter="|")

#bstart=54
#bend = 67
#df3 = df2[(df2['doc'] == 137)&(df2['start']==bstart)&(df2['end']==bend)]
#print df3['link']

#f2 = open("/home/adrian/git/error_analysis/tac/ruters-spotlight.csv", 'wb') 
#f2 = open("/home/adrian/git/error_analysis/tac/reuters-babelnet.csv", 'wb') 
#f2 = open("/home/adrian/git/error_analysis/tac/rbb-final.csv", 'wb') 

#f2 = open("/home/adrian/git/error_analysis/tac/kore50-spotlight.csv", 'wb') 
#f2 = open("/home/adrian/git/error_analysis/tac/kore50-babelnet.csv", 'wb') 
#f2 = open("/home/adrian/git/error_analysis/tac/kore50-aida.csv", 'wb') 

f2 = open("/home/adrian/git/error_analysis/tac/rbb-recognyze.csv", 'wb') 


def merge():
    links = {}
    
    try:
        for index, row in df1.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]
            #link = str(row[5])
            #doc = str(row[0])
            df3 = df2[(df2['doc']==row[0])&(df2['start']==row[1])&(df2['end']==row[2])&(df2['link']==row[5])]
            #&(df2['link']==row[5])
            print df3
            
            
            '''
            print link
            if links[link]:
                links[link][doc]+=1
                print 'updated key in dict'
            else:
                links[link][doc] = 0
                #links[link]
                print 'added new key'
            '''
            
            print row[0], row[1],row[2], row[5], df3.iloc[0]['type'], df3.iloc[0]['surfaceForm'], row[3], 0, 1 , 0, 0
            docno = str(row[0])
            start = str(row[1])
            end = str(row[2])
            link = str(row[5])
            type =  str(df3.iloc[0]['type'])
            surfaceForm = str(df3.iloc[0]['surfaceForm'])
            tac = str(row[3])
            #gold = str(row[2])
            S = str(0)
            B = str(0)
            A = str(0)
            R = str(0)
            
            #xf = float(row[2])
            if pd.isnull(row[4]):
                ingold = str(0)
                gold = ""
            else:
                ingold = str(1)
                gold = str(row[4])
        
            dn = int(docno)
            
            if dn<51:
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
                f2.write(ingold)
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

if __name__ == '__main__':
    print "start"

    merge()
    
    print "end"