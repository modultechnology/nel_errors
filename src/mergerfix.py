#!/usr/bin/python
# -*- coding: utf8 -*-

'''
This script creates unified tac-toolOutput file ready for merging.
Please note that the values for |S|B|A|R| will be 0 after running this script 
Please use the following header:
doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|goldLink|S|B|A|R|
or if it's only for Recognyze
doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|goldLink|
'''
from __future__ import division

import sys
import csv
import math

import pandas as pd


reload(sys)  
sys.setdefaultencoding('utf8')

#ANALYSIS
# doc|start|end|tac|gold|system|
#SYSTEM
# doc|start|end|link|score|type|surfaceForm|
#GOLD
# doc|start|end|gold|score|type|
#OVERLAP
#

#CASE 1 - TP - both in gold and system - correct link
#CASE 2 - FN - only in gold - missing,
#CASE 3 - FP - only in system - extra, wrong link

def get_concordance(textPath, start, end):
    cdistance = 10
    
    utf8_text=open(textPath,'r+').read()
    unitext = utf8_text.decode('utf8')

    textlen = len(unitext)

    if ((start - cdistance) > 0) and ((end + cdistance) < textlen):
        return unitext[(start - cdistance):(end + cdistance)]
    elif ((start - cdistance) > 0) and ((end + cdistance) > textlen):
        #this is outside the text's range...
        return ""
    elif (start - cdistance) < 0:
        if (end + cdistance) > textlen:
            return unitext[0:textlen]
        else:
            return unitext[0:(end + cdistance)]
    elif (end + cdistance) > textlen:
        if (start - cdistance) < 0:
            return unitext[0: textlen]
        else:
            return unitext[(start - cdistance): textlen]
    else:
        #any other case that's not covered - simply don't return anything
        return ""


def merge(folder, ds, file1, file2, gitbase):
    overlapCount = 0
    tpCount = 0
    fnCount = 0
    fpCount = 0
    
    #path, file1, file2, file3
    file1 = folder + '/' + file1
    file2 = folder + '/' + file2
    gold = folder + '/' + 'reuters128b.csv'
    over = folder + '/' + 'reuters128-overlap.csv'
    
    print folder
    print ds
    #this needs to be removed
    corpora = gitbase + '/' + 'nel_archive/corpora/' + ds + '/'
    print corpora
    
    #dfana - analysis (also contains gold)
    #dfsys - surfaceForms (does not contain gold)
    #therefore you need to check that any entry from dfana is contained in dfsys
    dfana = pd.read_csv(file1, delimiter="|")
    dfsys = pd.read_csv(file2, delimiter="|")
    dfgold = pd.read_csv(gold, delimiter="|")
    dfover = pd.read_csv(over, delimiter="|")
    
    #filePath = folder + ds + "-recognyze.csv"
    #f2 = open(filePath, 'wb') 
    
    #overlapPath = folder + ds + "-overlap.csv"
    #f3 = open(overlapPath, 'wb')
    
    Path = folder + '/' + ds + "-fixed.csv"
    f4 = open(Path, 'wb')
    
    print Path
    
    links = {}
    
    try:
        df1 = dfana[(dfana['tac']=='correct link')]
        tpCount = len(df1)
        
        df2 = dfana[(dfana['tac']=='missing')]
        fnCount = len(df2)
        
        df3 = dfana[(dfana['tac'].isin(['wrong-link','extra']))]
        fpCount = len(df3)
        
        #CORRECT LINK
        for index, row in df1.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]

            sysloc = dfsys[(dfsys['doc']==row[0]) & (dfsys['start']==row[1]) & (dfsys['end']==row[2])] 
                        
            done = 'a'
            if done=='a':
                print row[0], row[1],row[2], row[5], sysloc.iloc[0]['type'], sysloc.iloc[0]['surfaceForm'], row[3]#, 0, 1 , 0, 0
                docno = str(row[0])
                start = str(row[1])
                end = str(row[2])
                link = str(row[5])
                type =  str(sysloc.iloc[0]['type'])
                surfaceForm = str(sysloc.iloc[0]['surfaceForm'])
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
                
                f4.write(docno)
                f4.write("|")
                f4.write(start)
                f4.write("|")
                f4.write(end)
                f4.write("|")
                f4.write(link)  
                f4.write("|")    
                f4.write(type)
                f4.write("|")
                f4.write(surfaceForm)
                f4.write("|")
                f4.write(tac)  
                f4.write("|")
                #the next 2 are for error analysis
                #'''
                f4.write("||")
                #'''
                f4.write(ingold)
                f4.write("|")
                f4.write(gold)
                f4.write("|")
                
                textPath = corpora + docno + ".txt"
                concordance = get_concordance(textPath, int(start), int(end))
                
                #print concordance
                
                f4.write(concordance)
                f4.write("|")
                '''
                f4.write(S)  
                f4.write("|")    
                f4.write(B)
                f4.write("|")
                f4.write(A)
                f4.write("|")
                f4.write(R)  
                f4.write("|")
                #f4.write(score)
                #f4.write("|")
                '''
                f4.write("\n")
        
        #MISSING
        #there is no system results for this one, therefore we use gold
        for index, row in df2.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]  
                      
            goldloc = dfgold[(dfgold['doc']==row[0]) & (dfgold['start']==row[1]) & (dfgold['end']==row[2])]
                        
            #row[4] is gold link
            #locate the overlap
            overloc = dfover[(dfover['doc']==row[0]) & (dfover['gold']==row[4])]
            
            
            if not overloc.empty:   
                print "OVERLAP"
                
            else:
                print row[0], row[1],row[2], row[5], "", "", row[3]#, 0, 1 , 0, 0
                docno = str(row[0])
                start = str(row[1])
                end = str(row[2])
                link = str(row[5])

                if not goldloc.empty:
                    type =  str(goldloc.iloc[0]['type'])
                    surfaceForm = str(goldloc.iloc[0]['surfaceForm'])
                else:
                    type = "Undefined"
                    surfaceForm = ""
                
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
                
                f4.write(docno)
                f4.write("|")
                f4.write(start)
                f4.write("|")
                f4.write(end)
                f4.write("|")
                f4.write(link)  
                f4.write("|")    
                f4.write(type)
                f4.write("|")
                f4.write(surfaceForm)
                f4.write("|")
                f4.write(tac)  
                f4.write("|")
                #the next 2 are for error analysis
                #'''
                f4.write("||")
                #'''
                f4.write(ingold)
                f4.write("|")
                f4.write(gold)
                f4.write("|")
                
                textPath = corpora + docno + ".txt"
                concordance = get_concordance(textPath, int(start), int(end))
                
                #print concordance
                
                f4.write(concordance)
                f4.write("|")
                '''
                f4.write(S)  
                f4.write("|")    
                f4.write(B)
                f4.write("|")
                f4.write(A)
                f4.write("|")
                f4.write(R)  
                f4.write("|")
                #f4.write(score)
                #f4.write("|")
                '''
                f4.write("\n")
           
        #WRONG-LINK, EXTRA     
        #here surface should come from system
        for index, row in df3.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]

            sysloc = dfsys[(dfsys['doc']==row[0]) & (dfsys['start']==row[1]) & (dfsys['end']==row[2])]
            overloc = dfover[(dfover['doc']==row[0]) & (dfover['gold']==row[4]) & (dfover['tac']=='extra')]
            
            #do not write back the overlapping ones
            if not overloc.empty:
                print "OVERLAP!!!"
            else:
                print row[0], row[1],row[2], row[5], sysloc.iloc[0]['type'], sysloc.iloc[0]['surfaceForm'], row[3]#, 0, 1 , 0, 0
                
                overloc2 = dfover[(dfover['doc']==row[0]) & (dfover['start'] == row[1]) & (dfover['end']==row[2])]
                
                docno = str(row[0])
                start = str(row[1])
                end = str(row[2])
                link = str(row[5])
                type =  str(sysloc.iloc[0]['type'])
                surfaceForm = str(sysloc.iloc[0]['surfaceForm'])
                
                if not overloc2.empty:
                    tac = 'correct link'
                else:
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
                
                f4.write(docno)
                f4.write("|")
                f4.write(start)
                f4.write("|")
                f4.write(end)
                f4.write("|")
                f4.write(link)  
                f4.write("|")    
                f4.write(type)
                f4.write("|")
                f4.write(surfaceForm)
                f4.write("|")
                f4.write(tac)  
                f4.write("|")
                #the next 2 are for error analysis
                #'''
                f4.write("||")
                #'''
                f4.write(ingold)
                f4.write("|")
                f4.write(gold)
                f4.write("|")
                
                textPath = corpora + docno + ".txt"
                concordance = get_concordance(textPath, int(start), int(end))
                
                #print concordance
                
                f4.write(concordance)
                f4.write("|")
                '''
                f4.write(S)  
                f4.write("|")    
                f4.write(B)
                f4.write("|")
                f4.write(A)
                f4.write("|")
                f4.write(R)  
                f4.write("|")
                #f4.write(score)
                #f4.write("|")
                '''
                f4.write("\n")              
             
    finally:
        f4.close()
    return tpCount, fpCount, fnCount, overlapCount

if __name__ == '__main__':
    print "start"

    tpCount, fpCount, fnCount, overlapCount = merge(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    
    print "end"
    print "returned TP, FN, FP"
    print tpCount
    print fnCount
    print fpCount
    print overlapCount
    
    print "results"
    print (tpCount)/(tpCount+fpCount)
    print (tpCount)/(tpCount+fnCount)
    print (2*tpCount)/(2*tpCount+fpCount+fnCount)
    
    
    tpCount = tpCount + overlapCount
    fnCount = fnCount - overlapCount
    fpCount = fpCount - overlapCount
    
    print "real TP, FN, FP"
    print tpCount
    print fnCount
    print fpCount
    
    #'''
    print "real results"
    pr = 0
    recall = 0
    f1 = 0
    
    pr = (tpCount)/(tpCount+fpCount)
    recall = (tpCount)/(tpCount+fnCount)
    f1 = (2*tpCount)/(2*tpCount+fpCount+fnCount)
    
    print pr
    print recall
    print f1
    #'''