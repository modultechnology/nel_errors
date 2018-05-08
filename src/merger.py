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
import string
import regex as re
import pandas as pd

def remove_punctuation(text):
    return re.sub(ur"\p{P}+", "", text)

reload(sys)  
sys.setdefaultencoding('utf8')

#ANALYSIS
# doc|start|end|tac|gold|system|
#SYSTEM
# doc|start|end|link|score|type|surfaceForm|
#GOLD
# doc|start|end|gold|score|type|

#CASE 1 - TP - both in gold and system - correct link
#CASE 2 - FN - only in gold - missing,
#CASE 3 - FP - only in system - extra, wrong link

def merge(folder, ds, file1, file2):
    '''
    overlapCount = 0
    tpCount = 0
    fnCount = 0
    fpCount = 0
    
    overlapPerson = 0
    tpPerson = 0
    fnPerson = 0
    fpPerson = 0
    
    overlapLocation = 0
    tpLocation = 0
    fnLocation = 0
    fpLocation = 0
    
    
    overlapOrganisation = 0
    tpOrganisation = 0
    fnOrganisation = 0
    fpOrganisation = 0
    '''
    
    #path, file1, file2, file3
    file1 = folder + file1
    file2 = folder + file2
    gold = folder + ds + 'a.csv'
    
    #dfana - analysis (also contains gold)
    #dfsys - surfaceForms (does not contain gold)
    #therefore you need to check that any entry from dfana is contained in dfsys
    
    print file1
    print file2
    
    dfana = pd.read_csv(file1, delimiter="|")
    dfsys = pd.read_csv(file2, delimiter="|")
    dfgold = pd.read_csv(gold, delimiter="|")
    
    filePath = folder + ds + "-recognyze.csv"
    f2 = open(filePath, 'wb') 
    
    overlapPath = folder + ds + "-overlap.csv"
    f3 = open(overlapPath, 'wb')
    
    #resByTypePath = folder + ds + "-resultsbytype.txt"
    #fresults = open(resByTypePath, 'wb')
    
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
            
                #dn = int(docno)
                
                '''
                if type=='Person':
                    tpPerson += 1
                elif type=='Location':
                    tpLocation += 1
                elif type== 'Organisation':
                    tpOrganisation += 1
                '''
                
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
                #the next 2 are for error analysis
                #'''
                f2.write("||")
                #'''
                f2.write(ingold)
                f2.write("|")
                f2.write(gold)
                f2.write("|")
                '''
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
                '''
                f2.write("\n")
        
        #MISSING
        for index, row in df2.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]  
                      
            #there is no system results for this one, therefore we use gold
            goldloc = dfgold[(dfgold['doc']==row[0]) & (dfgold['start']==row[1]) & (dfgold['end']==row[2])]
            #dfOverlap = dfgold[(dfgold['doc']==row[0]) & (dfgold['gold']==row[5])]
            #dfOverlapGold = dfgold[(dfgold['doc']==row[0]) & (dfgold['gold']==row[5]) & (dfgold['start']>=row[1]) & (dfgold['start']<=row[2])]
           
            done = 'a'
            if done=='a':
                #print row[0], row[1],row[2], row[5], goldloc.iloc[0]['type'], "", row[3]
                #, 0, 1 , 0, 0
                docno = str(row[0])
                start = str(row[1])
                end = str(row[2])
                link = str(row[5])
                print len(goldloc.iloc[0])
                print goldloc.iloc[0]
                print goldloc.iloc[0]['type']
                type =  str(goldloc.iloc[0]['type'])
                surfaceForm = str("")
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
                
                '''
                if type=='Person':
                    fnPerson += 1
                    #overlapPerson += 1
                elif type=='Location':
                    fnLocation += 1
                    #overlapLocation += 1
                elif type== 'Organisation':
                    fnOrganisation += 1
                    #overlapOrganisation += 1
                '''
            
                #dn = int(docno)
                
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
                #the next 2 are for error analysis
                #'''
                f2.write("||")
                #'''
                f2.write(ingold)
                f2.write("|")
                f2.write(gold)
                f2.write("|")
                
                '''
                #write start and end for the overlap - if available
               
                if not dfOverlapGold.empty:
                    f3.write(str(dfOverlapGold.iloc[0]['start']))
                    f3.write("|")
                    f3.write(str(dfOverlapGold.iloc[0]['end']))
                    f3.write("|")
                
                elif not dfOverlap.empty:
                    f3.write(str(dfOverlap.iloc[0]['start']))
                    f3.write("|")
                    f3.write(str(dfOverlap.iloc[0]['end']))
                    f3.write("|")
                
                
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
                '''
                f2.write("\n")
           
        #WRONG-LINK, EXTRA     
        for index, row in df3.iterrows():
            print row[0], row[1], row[2], row[3], row[4], row[5]

            sysloc = dfsys[(dfsys['doc']==row[0]) & (dfsys['start']==row[1]) & (dfsys['end']==row[2])]
            dfOverlap = dfgold[(dfgold['doc']==row[0]) & (dfgold['gold']==row[5])]
            dfOverlapGold = dfgold[(dfgold['doc']==row[0]) & (dfgold['gold']==row[5]) & (dfgold['start']>=row[1]) & (dfgold['start']<=row[2])]
            
            if not dfOverlap.empty:
                #overlapCount += 1
                #print row[0], row[1],row[2], row[5], sysloc.iloc[0]['type'], sysloc.iloc[0]['surfaceForm'], row[3]
                #, 0, 1 , 0, 0
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
                '''
                if pd.isnull(row[4]):
                    ingold = str(0)
                    gold = ""
                else:
                    ingold = str(1)
                    #gold = str(row[4])
                    gold = str(dfOverlap.iloc[0]['gold'])
                '''
                #we set ingold as 2 - this describes the fact that it's a partial match
                #we usually don't have a gold here, therefore we take it from overlap
                #we simply check at the start or the end of the interval....
                ingold = str(2)
                if not dfOverlapGold.empty:
                    gold = str(dfOverlapGold.iloc[0]['gold'])
                else:
                    gold = str(dfOverlap.iloc[0]['gold'])
                
                    
                '''
                if type=='Person':
                    fpPerson += 1
                    overlapPerson += 1
                elif type=='Location':
                    fpLocation += 1
                    overlapLocation += 1
                elif type== 'Organisation':
                    fpOrganisation += 1
                    overlapOrganisation += 1    
                '''
                
                #we only keep extras for inclusion in gold standards as wrong-links imply a more serious error
                #(e.g., Ford Motor Company and Patrick Ford - could be wrong links, but they're definitely different entities)
                if (tac=='extra'):
                    #dn = int(docno)
                    f3.write(docno)
                    f3.write("|")
                    f3.write(start)
                    f3.write("|")
                    f3.write(end)
                    f3.write("|")
                    f3.write(link)  
                    f3.write("|")    
                    f3.write(type)
                    f3.write("|")
                    f3.write(surfaceForm)
                    f3.write("|")
                    if not dfOverlapGold.empty:
                        f3.write(tac)
                    else:
                        f3.write('goldmissing')  
                    f3.write("|")
                    #the next 2 are for error analysis
                    #'''
                    f3.write("||")
                    #'''
                    if not dfOverlapGold.empty:
                        f3.write(ingold)
                    else:
                        f3.write(str(3))
                        
                    f3.write("|")
                    f3.write(gold)
                    f3.write("|")
                    
                    
                    #write start and end for the overlap - if available
                    if not dfOverlapGold.empty:
                        f3.write(str(dfOverlapGold.iloc[0]['start']))
                        f3.write("|")
                        f3.write(str(dfOverlapGold.iloc[0]['end']))
                        f3.write("|")

                    else:
                        f3.write(str(dfOverlap.iloc[0]['start']))
                        f3.write("|")
                        f3.write(str(dfOverlap.iloc[0]['end']))
                        f3.write("|")
                    
                    
                    
                    '''
                    f3.write(S)  
                    f3.write("|")    
                    f3.write(B)
                    f3.write("|")
                    f3.write(A)
                    f3.write("|")
                    f3.write(R)  
                    f3.write("|")
                    #f3.write(score)
                    #f3.write("|")
                    '''
                    f3.write("\n")          
                
            else:
                if not sysloc.empty:
                    #print row[0], row[1],row[2], row[5], sysloc.iloc[0]['type'], sysloc.iloc[0]['surfaceForm'], row[3]
                    #, 0, 1 , 0, 0
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
                    
                    '''
                    if type=='Person':
                        fpPerson += 1
                    elif type=='Location':
                        fpLocation += 1
                    elif type== 'Organisation':
                        fpOrganisation += 1
                    '''
                    #dn = int(docno)
                    
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
                    #the next 2 are for error analysis
                    #'''
                    f2.write("||")
                    #'''
                    f2.write(ingold)
                    f2.write("|")
                    f2.write(gold)
                    f2.write("|")
                    
                    
                    #write start and end for the overlap - if available
                    if not dfOverlapGold.empty:
                        f3.write(str(dfOverlapGold.iloc[0]['start']))
                        f3.write("|")
                        f3.write(str(dfOverlapGold.iloc[0]['end']))
                        f3.write("|")

                    '''
                    else:
                        f3.write(str(dfOverlap.iloc[0]['start']))
                        f3.write("|")
                        f3.write(str(dfOverlap.iloc[0]['end']))
                        f3.write("|")
                        
                    
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
                    '''
                    f2.write("\n")              
            
        
            
    finally:
        f2.close()
        
    '''
    tpCount = tpCount + overlapCount
    fnCount = fnCount - overlapCount
    fpCount = fpCount - overlapCount
    
    pr = (tpCount)/(tpCount+fpCount)
    recall = (tpCount)/(tpCount+fnCount)
    f1 = (2*tpCount)/(2*tpCount+fpCount+fnCount)
    
    print pr
    print recall
    print f1
    '''
    
    '''
    fresults.write("TYPE \n")
    fresults.write("OVERLAP \n")
    fresults.write("TP, FN, FP \n")
    fresults.write("P, R, F1 \n")
    fresults.write("\n")

   
    tpLocation = tpLocation + overlapLocation
    fnLocation = fnLocation - overlapLocation
    fpLocation = fpLocation - overlapLocation
    pr, recall, f1 = measures(tpLocation, fnLocation, fpLocation)
    
    fresults.write("Location \n")
    fresults.write(str(overlapLocation))
    fresults.write("\n")
    fresults.write(str(tpLocation) + " ")
    fresults.write(str(tpLocation) + " ")
    fresults.write(str(tpLocation) + " ")
    fresults.write("\n")
    fresults.write(str(pr)+ " ")
    fresults.write(str(recall)+ " ")
    fresults.write(str(f1)+ " ")
    fresults.write("\n")
    fresults.write("\n")
        
    print "PERSON"

    tpPerson = tpPerson + overlapPerson
    fnPerson = fnPerson - overlapPerson
    fpPerson = fpPerson - overlapPerson
    pr, recall, f1 = measures(tpPerson, fnPerson, fpPerson)
    
    fresults.write("Person \n")
    fresults.write(str(overlapPerson))
    fresults.write("\n")
    fresults.write(str(tpPerson) + " ")
    fresults.write(str(fnPerson)+ " ")
    fresults.write(str(fpPerson)+ " ")
    fresults.write("\n")
    fresults.write(str(pr)+ " ")
    fresults.write(str(recall)+ " ")
    fresults.write(str(f1)+ " ")
    fresults.write("\n")
    fresults.write("\n")
        
        
    print "ORGANISATION"
    tpOrganisation = tpOrganisation + overlapOrganisation
    fnOrganisation = fnOrganisation - overlapOrganisation
    fpOrganisation = fpOrganisation - overlapOrganisation
    pr, recall, f1 = measures(tpOrganisation, fnOrganisation, fpOrganisation)
    
    fresults.write("Organisation \n")
    fresults.write(str(overlapOrganisation))
    fresults.write("\n")
    fresults.write(str(tpOrganisation)+ " ")
    fresults.write(str(fnOrganisation)+ " ")
    fresults.write(str(fpOrganisation)+ " ")
    fresults.write("\n")
    fresults.write(str(pr)+ " ")
    fresults.write(str(recall)+ " ")
    fresults.write(str(f1)+ " ")
    fresults.write("\n")
    fresults.write("\n")
    fresults.close()
    
    
    return tpCount, fpCount, fnCount, overlapCount
    '''

def measures(tp, fn, fp):
    
    pr = (tp)/(tp+fp)
    recall = (tp)/(tp+fn)
    f1 = (2*tp)/(2*tp+fp+fn)
    
    return pr, recall, f1



if __name__ == '__main__':
    print "start"

    #tpCount, fpCount, fnCount, overlapCount = 
    merge(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    