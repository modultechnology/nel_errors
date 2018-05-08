#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import division

import sys
import csv
import math
import string
import regex as re
import pandas as pd


def fixer(overlapfile, fixedfile):
    tp = 0
    fp = 0
    fn = 0
    
    gmPerson = 0
    overlapPerson = 0
    tpPerson = 0
    fpPerson = 0
    fnPerson = 0
    
    gmLocation = 0
    overlapLocation = 0
    tpLocation = 0
    fpLocation = 0
    fnLocation = 0
    
    gmOrganisation = 0
    overlapOrganisation = 0
    tpOrganisation = 0
    fpOrganisation = 0
    fnOrganisation = 0
    
    gmUndefined = 0
    overlapUndefined = 0
    tpUndefined = 0
    fpUndefined = 0
    fnUndefined = 0
    
    with open(overlapfile) as overfile:
        for line in overfile:
            if "extra" in line:
                if "Person" in line:
                    overlapPerson += 1
                elif "Organisation" in line:
                    overlapOrganisation += 1
                elif "Location" in line:
                    overlapLocation +=1
                else:
                    overlapUndefined +=1
            elif "goldmiss" in line:
                if "Person" in line:
                    gmPerson += 1
                elif "Organisation" in line:
                    gmOrganisation += 1
                elif "Location" in line:
                    gmLocation +=1
                else:
                    gmUndefined +=1

    with open(fixedfile) as origin:
        for line in origin:
            if "correct link" in line:
                tp +=1
                
                if "Person" in line:
                    tpPerson +=1
                elif "Location" in line:
                    tpLocation += 1
                elif "Organisation" in line:
                    tpOrganisation += 1
                elif "Undefined" in line:
                    tpUndefined += 1
                
            elif "missing" in line:
                fn +=1
                
                if "Person" in line:
                    fnPerson +=1
                elif "Location" in line:
                    fnLocation += 1
                elif "Organisation" in line:
                    fnOrganisation += 1
                elif "Undefined" in line:
                    fnUndefined += 1
                    
            elif "extra" or "wrong-link" in line:
                fp +=1
                
                if "Person" in line:
                    fpPerson +=1
                elif "Location" in line:
                    fpLocation += 1
                elif "Organisation" in line:
                    fpOrganisation += 1
                elif "Undefined" in line:
                    fpUndefined += 1
              
            '''      
            try:
                print line.split('"')[1]
            except IndexError:
            '''
    
    print "TYPE"
    print "OVERLAP"
    print "GOLDMISSING"
    print "TP, FP, FN"
    print "P, R, F1"
    
    #overlapUndefined -= 1

    overlapAll = overlapPerson + overlapLocation + overlapOrganisation + overlapUndefined
    gmAll = gmPerson + gmLocation + gmOrganisation + gmUndefined
    print "\n"
    print "Overall"
    print overlapAll
    print gmAll
    print tp, fp, fn
    pr, recall, f1 = measures(tp, fp, fn)
    print pr, recall, f1


    print "\n"
    print "Location"
    print overlapLocation
    print gmLocation
    print tpLocation, fpLocation, fnLocation
    pr, recall, f1 = measures(tpLocation, fpLocation, fnLocation)
    print pr, recall, f1  
    
    print "\n"
    print "Person"
    print overlapPerson
    print gmPerson
    print tpPerson, fpPerson, fnPerson
    pr, recall, f1 = measures(tpPerson, fpPerson, fnPerson)
    print pr, recall, f1
    
    print "\n"
    print "Organisation"
    print overlapOrganisation
    print gmOrganisation
    print tpOrganisation, fpOrganisation, fnOrganisation
    pr, recall, f1 = measures(tpOrganisation, fpOrganisation, fnOrganisation)
    print pr, recall, f1    
    
    print "\n"
    print "Undefined"
    print overlapUndefined
    print gmUndefined
    print tpUndefined, fpUndefined, fnUndefined
    
        
def measures(tp, fn, fp):
    pr = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = (2*tp)/(2*tp+fp+fn)
    
    return pr, recall, f1
    

if __name__ == '__main__':
    #print "start"
    
    #format: dataset profile path
    #main()
    fixer(sys.argv[1], sys.argv[2])

    
    #print "end"