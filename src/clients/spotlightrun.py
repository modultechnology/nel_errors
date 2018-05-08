#!/usr/bin/python
# -*- coding: utf-8 -*-
import spotlight

import os
import nltk
import csv
import urllib2
import urllib
import json
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

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_annotations(dataset, gitpath, tool):
    print "start SPOTLIGHT eval"
    import spotlight
    annos = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate', 'Donald Trump won the elections', confidence=0.4, support=20) 
    print annos
    
    mypath = gitpath + "/error_analysis/corpora/" + dataset + "/gold/" + dataset + "gold.csv"
    results = gitpath + "/error_analysis/results/" + tool + "/" + dataset + "/"
    
    #'''
    LANG_PORTS = {
        "english": '2222',
        "german": '2226',
        "dutch": '2232',
        "hungarian": '2229',
        "french": '2225',
        "portuguese": '2228',
        "italian": '2230',
        "russian": '2227',
        "turkish": '2235',
        "spanish": '2231'
    }
    
    client = 'http://spotlight.sztaki.hu:2222/rest/annotate'
    print client
    
    only_pol_filter = {
                    'policy': 'whitelist',
                    'types': 'DBpedia:Person, DBpedia:Place, DBpedia:Location, DBpedia:Organisation, Http://xmlns.com/foaf/0.1/Person',
                    'coreferenceResolution': True
                    }
    
    print "start"
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        
    for f in onlyfiles:
        #print f
        with open(os.path.join(mypath, f), 'rb') as textfile:
            fileno = f.split('.')[0]
            current=textfile.read()
            #text = current
           
            #spotlight.annotate(client, current, confidence=0.4, support=20)
            print 'file:' + fileno
            try:
                data = spotlight.annotate(client, text=current, confidence=0.4, support=20,
                                          filters=only_pol_filter)
                #run rbb - confidence = 0.5, support = 50
                #run rbb2 - confidence = 0.5, support = 40
                
                if len(data)>0:
                    with open(results + dataset + "/" + fileno+'.json', 'w') as resfile:
                        json.dump(data, resfile)
            except spotlight.SpotlightException as werr:
                logger.warn("SpotlightException: {}".format(werr.message))


def get_dbpedia_type(types):
    res = "Other"
    if types!="":
        for type in types.split(","):
            #print type
            if type in ('Http://xmlns.com/foaf/0.1/Person','DBpedia:Person'):
                res = 'Person'
            if type in ('DBpedia:Place','DBpedia:Location'):
                res = 'Location'
            if type in ('DBpedia:Organisation'):
                res = 'Organisation'
    return res

def convert_annotations(folder, run, dataset, surface):
    results = folder + dataset
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
                for rs in d:
                    #print rs
                    #print rs[u'offset']
                    #print 'end:', (rs[u'offset'] + len(rs[u'surfaceForm'])) 
                    #print rs[u'offset']+len(rs[u'surfaceForm'])
                    
                    #'''
                    
                    #print("surfaceForm:", rs['surfaceForm'])
                    #print("type:", type(rs['surfaceForm']))
                    if  isinstance(rs[u'surfaceForm'], int):
                        some_Val = rs[u'surfaceForm']
                        rs[u'surfaceForm'] = str(rs[u'surfaceForm'])
                        pass
                    else:
                        end = rs[u'offset'] + len(rs[u'surfaceForm'])
                        #print rs[u'offset']
                        #print end
                    
                    #docno = int(anno.split(".")[0])
                    docno = 100
                    if docno!=51:
                    #if docno < 51:
                        print docno
                        csvrun.write(anno.split(".")[0])
                        csvrun.write("|")
                        csvrun.write(str(rs[u'offset']))
                        csvrun.write("|")
                        csvrun.write(str(end))
                        csvrun.write("|")
                        csvrun.write(urllib.unquote(rs[u'URI']).encode("utf8"))
                        csvrun.write("|")
                        csvrun.write("1")
                        csvrun.write("|")
                        csvrun.write(get_dbpedia_type(rs[u'types']))
                        csvrun.write("|")
                        #csvrun.write(rs[u'surfaceForm'].encode("utf8"))
                        if surface == True:
                            csvrun.write(rs[u'surfaceForm'].encode("utf8"))
                            csvrun.write("|")
                            #'''
                        csvrun.write("\n")
                    #'''
    print("end ca")

def main(argv):
    #these are outdated
    #get_annotations(dataset)
    #convert_annotations(results, run2)
    #print get_dbpedia_type("Schema:Place,DBpedia:Place,DBpedia:PopulatedPlace,Schema:Country,DBpedia:Country")
    
    
    evalpath = ''
    dataset = ''
    profile = ''
    gitpath = ''
    
    try:
        opts, args = getopt.getopt(argv,"he:d:p:",["evalpath=","dataset=","profile=","gitpath="])
    except getopt.GetoptError:
        print 'datasetuploader.py -p <evalpath> -d <dataset> -p <profile> -g <gitpath>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'datasetuploader.py -p <evalpath> -d <dataset> -p <profile> -g <gitpath>'
            sys.exit()
        elif opt in ("-e", "--evalpath"):
            evalpath = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
        elif opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-g", "--gitpath"):
            profile = arg
            
    print 'Path is: ', evalpath
    print 'Dataset is: ', dataset
    print 'Profile is:', profile
    print 'Gitpath is:', gitpath
    
    
    #get_annotations(dataset, gitpath, tool)
    
    convert_annotations(evalpath +"/runs/", evalpath +"/" + dataset +"-" + profile + ".csv", dataset, False)
    convert_annotations(evalpath +"/runs/", evalpath +"/" + dataset +"-" + profile + "-surface.csv", dataset, True)

    #convert_annotations(results, run+".csv", False)
    #convert_annotations(results, run2+"surface.csv", True)
    

if __name__ == '__main__':
    print "start"
    
    #format: dataset profile path
    #main()
    main(sys.argv[1:])
    
    print "end"