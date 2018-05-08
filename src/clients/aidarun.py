#!/usr/bin/python
# -*- coding: utf8 -*-
import requests
import os
import nltk
import csv
import json
import urllib
import logging
import sys
import getopt
from os import listdir
from os.path import isfile, join

from pprint import pprint
from StringIO import StringIO
from sets import Set

reload(sys)  
sys.setdefaultencoding('utf8')




'''
gitpath = "/home/git/"

title = "reuters128"
mypath = gitpath + "error_analysis/corpora/reuters128/corpora/"
goldfile = gitpath + "error_analysis/corpora/reuters128/gold/reuters128goldmain.csv"
results = gitpath + "error_analysis/results2/aida/"
run = gitpath + "error_analysis/runs/aida/reuters128run-aida1.csv"
run2 = gitpath + "error_analysis/runs/aida/reuters128run-aida2.csv"
'''

text = 'Dylan was born in Duluth.'

def get_annotations():
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        
    for f in onlyfiles:
        #print f
        with open(os.path.join(mypath, f), 'rb') as textfile:
            fileno = f.split('.')[0]
            print fileno
            current=textfile.read()
            data = {
              'text': current
            } 
    
            r = requests.post('https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate', data=data)
            print(r.json())
            
            with open(results + title + "/" + fileno+'.json', 'w') as resfile:
                json.dump(r.json(), resfile)

def get_dbpedia_type(types):
    #this works under the assumption that YAGO types are correct
    #the name probably should be get_yago_type
    res = "notype"
    for type in types:
        #print type
        if type in ('YAGO_wordnet_person_100007846'):
            res = 'Person'
        if type in ('YAGO_yagoGeoEntity'):
            res = 'Location'
        if type in ('YAGO_wordnet_organization_108008335'):
            res = 'Organisation'
    return res

def convert_annotations(folder, run, surface):
    results = folder + title
    print results
    onlyfiles2 = [ f for f in listdir(results) if isfile(join(results,f)) ]
    
    with open(run, 'a') as csvrun:
    
        #take only results that are fps
        for f in onlyfiles2:
            anno = f.split("-")[0]
            print anno
            with open(os.path.join(results, f), 'rb') as json_data:
                d = json.load(json_data)
                print d #print len(d)
                for rs in d['mentions']:
                    if len(rs['allEntities'])>0:
                        csvrun.write(anno.split(".")[0])
                        csvrun.write("|")
                        csvrun.write(str(rs['offset']))
                        csvrun.write("|")
                        csvrun.write(str(rs['offset'] + rs['length']))
                        csvrun.write("|")
                        emet = rs['allEntities'][0]['kbIdentifier']
                        #url = d['entityMetadata'][emet]['url']
                        #print url.replace("en.wikipedia.org/wiki","dbpedia.org/resource").encode("utf8")
                        #apparently YAGO URLs correspond quite well to DBpedia URLs
                        dbpurl = ("http://dbpedia.org/resource/" + emet.split(":")[1]).encode("utf8")
                        #print dbpurl
                        csvrun.write(urllib.unquote(dbpurl))
                        csvrun.write("|")
                        csvrun.write("1")
                        csvrun.write("|")
                        csvrun.write(get_dbpedia_type(d['entityMetadata'][emet]['type']))
                        csvrun.write("|")
                        if surface == True:
                            csvrun.write(rs[u'name'])
                            csvrun.write("|")
                        csvrun.write("\n")
                #for rs in d:
                #    print rs
                '''
                    csvrun.write(anno.split(".")[0])
                    csvrun.write("|")
                    csvrun.write(str(rs['charFragment']['start']))
                    csvrun.write("|")
                    csvrun.write(str(rs['charFragment']['end']))
                    csvrun.write("|")
                    csvrun.write(urllib.unquote(rs['DBpediaURL']).encode("utf8"))
                    csvrun.write("|")
                    csvrun.write("1")
                    csvrun.write("|")
                    csvrun.write(get_dbpedia_type("http://dbpedia.org/sparql", rs['DBpediaURL']))
                    csvrun.write("|")
                    csvrun.write("\n")
                '''
    print("end ca")

    
#if __name__ == '__main__':
    #print "start"
    #get_annotations()
    #get_dbpedia_type()
    #convert_annotations(results, run)
    #convert_annotations(results, run2)

             
#def main(argv):
def main(argv):
    #in order to run this:
    #python recognyzeclient2.py -e /home/adrian/git/nel_archive/20170204/test -d reuters128 -p advanced
    
    #get_annotations()
    #print get_dbpedia_type("Schema:Place,DBpedia:Place,DBpedia:PopulatedPlace,Schema:Country,DBpedia:Country")
    #convert_annotations(results, run)
    
    #results = "/home/adrian/git/nel_archive/20170204/test/runs/"
    # $4 + "runs"
    #run = "/home/adrian/git/error_analysis/runs/recognyze/new/reuters128run-recognyze-"
    # $4 + $2 + "-" + $3 + ".csv"
    # $4 + $2 + "-" + $3 + "-surface.csv"
    #path + dataset + profile 
    
    evalpath = ''
    dataset = ''
    profile = ''
    
    try:
        opts, args = getopt.getopt(argv,"he:d:p:",["evalpath=","dataset=","profile="])
    except getopt.GetoptError:
        print 'datasetuploader.py -p <evalpath> -d <dataset> -p <profile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'datasetuploader.py -p <evalpath> -d <dataset> -p <profile>'
            sys.exit()
        elif opt in ("-e", "--evalpath"):
            evalpath = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
        elif opt in ("-p", "--profile"):
            profile = arg
            
    print 'Path is: ', evalpath
    print 'Dataset is: ', dataset
    print 'Profile is:', profile
    
    convert_annotations(evalpath +"/runs/", evalpath +"/" + dataset +"-" + profile + ".csv", False)
    convert_annotations(evalpath +"/runs/", evalpath +"/" + dataset +"-" + profile + "-surface.csv", True)

    #convert_annotations(results, run+".csv", False)
    #convert_annotations(results, run2+"surface.csv", True)


if __name__ == '__main__':
    print "start"
    
    #format: dataset profile path
    #main()
    main(sys.argv[1:])
    
    print "end"
