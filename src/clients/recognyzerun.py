#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from SPARQLWrapper import SPARQLWrapper, JSON
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

def get_annotations():
    ''''
    right there is no need to implement this method as we already have the runs
    '''
    return ""


def get_dbpedia_type(types):
    res = "notype"
    if types!="":
        for type in types.split(","):
            #print type
            if type in ('http://xmlns.com/foaf/0.1/Person','DBpedia:Person'):
                res = 'Person'
            if type in ('DBpedia:Place','DBpedia:Location'):
                res = 'Location'
            if type in ('DBpedia:Organisation'):
                res = 'Organisation'
    return res

#TODO: check we get the correct types from DBpedia
def get_dbpedia_type(lang, uri):
        '''
        Get a German URI via an English DBpedia URI.
        There are cases where multiple URIs are returned, but we only take the first one.
        :param uri: a DBpedia URI.
        :returns: German DBpedia URI
        '''
        #print "get city location using DBpedia uri"
        #here you have to decode the string first, not encode it
        #print uri
        res = 'notype'
        sparql = SPARQLWrapper(lang)
        sparql.setQuery('''
        SELECT DISTINCT ?obj
        WHERE {
        <'''+urllib.unquote(uri).encode("utf8")+'''> (rdf:type)* ?obj
        }
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results:
            for result in results["results"]["bindings"]:
                #print result["obj"]["value"]
                '''
                #dbo:Place, dbo:Location, geo:SpatialThing
                if ('http://dbpedia.org/ontology/Place') in result["obj"]["value"]:
                    res = 'Location'
                if ('http://dbpedia.org/ontology/Location') in result["obj"]["value"]:
                    res = 'Location'
                if ('http://dbpedia.org/class/yago/YagoGeoEntity') in result["obj"]["value"]:
                    res = 'Location'
                #dbo:Person, foaf:Person
                if ('http://dbpedia.org/ontology/Person') in result["obj"]["value"]:
                    res = 'Person'
                if ('http://xmlns.com/foaf/0.1/Person') in result["obj"]["value"]:
                    res = 'Person'
                #dbo:Organisation - and possibly several other types
                if ('http://dbpedia.org/ontology/Organisation') in result["obj"]["value"]:
                    res = 'Organisation'
                if ('http://dbpedia.org/class/yago/Organization108008335') in result["obj"]["value"]:
                    res = 'Organisation'
                '''
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Place', 'http://dbpedia.org/ontology/Location', 'http://dbpedia.org/class/yago/YagoGeoEntity'):
                    res = 'Location'
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Person', 'http://xmlns.com/foaf/0.1/Person'):
                    res = 'Person'
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Organisation', 'http://dbpedia.org/class/yago/Organization108008335'):
                    res = 'Organisation'
        
        #print res
        return res
    
def get_dbpedia_type2(rtype):
    if rtype == 'http://schema.org/Place': 
        type = 'Location'
    elif rtype == 'http://schema.org/Person':
        type = 'Person'
    elif rtype == 'http://schema.org/Organization':
        type = 'Organisation'
    else:
        type = 'notype'
    
    return type

def convert_annotations_old(folder, run, dataset, surface):
    results = folder + dataset
    print "start dbpedia queries"
    #print results
    onlyfiles2 = [ f for f in listdir(results) if isfile(join(results,f)) ]
    
    with open(run, 'a') as csvrun:
    
        #take only results that are fps
        for f in onlyfiles2:
            anno = f.split("-")[0]
            #print anno
            with open(os.path.join(results, f), 'rb') as json_data:
                d = json.load(json_data)
                #print d #print len(d)
                for rs in d:
                    #print rs
                    #print rs[u'offset']
                    #print 'end:', (rs[u'offset'] + len(rs[u'surfaceForm'])) 
                    #print rs[u'offset']+len(rs[u'surfaceForm'])
                    
                    #'''
                    
                    '''
                    print("surfaceForm:", rs[u'surfaceForms'])
                    print("type:", type(rs[u'key']))
                    
                    if  isinstance(rs[u'surfaceForm'], int):
                        pass
                    else:
                        end = rs[u'offset'] + len(rs[u'surfaceForm'])
                        print rs[u'offset']
                        print end
                    '''
                    for form in rs[u'surfaceForms']: 
                        if "Suchoi" not in rs[u'key']:
                            csvrun.write(anno.split(".")[0])
                            csvrun.write("|")
                            csvrun.write(str(form[u'startIndex']-1))
                            csvrun.write("|")
                            csvrun.write(str(form[u'endIndex']-1))
                            csvrun.write("|")
                            csvrun.write(urllib.unquote(rs[u'key']).encode("utf8"))
                            csvrun.write("|")
                            csvrun.write("1")
                            csvrun.write("|")
                            #csvrun.write(get_dbpedia_type("http://dbpedia.org/sparql", rs[u'key']))
                            csvrun.write(get_dbpedia_type2(rs[u'entity_type']))
                            csvrun.write("|")
                            if surface == True:
                                csvrun.write(rs[u'surfaceForm'].encode("utf8"))
                                csvrun.write("|")
                            #'''
                            csvrun.write("\n")
                    #'''
    print("finished dbpedia queries")


def convert_annotations(folder, run, dataset, surface):
    results = folder + dataset
    print "start dbpedia queries"
    #print results
    onlyfiles2 = [ f for f in listdir(results) if isfile(join(results,f)) ]
    
    with open(run, 'a') as csvrun:
    
        #take only results that are fps
        for f in onlyfiles2:
            anno = f.split("-")[0]
            #print anno
            with open(os.path.join(results, f), 'rb') as json_data:
                d = json.load(json_data)
                #print d #print len(d)
                for rs in d:
                    
                    #for em in rs['entity_metadata']: 
                    if "Suchoi" not in rs['key']:
                        csvrun.write(anno.split(".")[0])
                        csvrun.write("|")
                        csvrun.write(rs['entity_metadata']['document_index_start'][0])
                        csvrun.write("|")
                        csvrun.write(rs['entity_metadata']['document_index_end'][0])
                        csvrun.write("|")
                            
                    csvrun.write(urllib.unquote(rs['key']).encode("utf8"))
                    csvrun.write("|")
                    csvrun.write("1")
                    csvrun.write("|")
                    #csvrun.write(get_dbpedia_type("http://dbpedia.org/sparql", rs[u'key']))
                    csvrun.write(get_dbpedia_type2(rs['entity_type']))
                    csvrun.write("|")
                    if surface == True:
                        csvrun.write(rs['surfaceForm'].encode("utf8"))
                        csvrun.write("|")
                            #'''
                    csvrun.write("\n")
                    #'''
    print("finished dbpedia queries")

#def main(argv):
def main(argv):
    #in order to run this check the bash files from nel_archive
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