#!/usr/bin/python
# -*- coding: utf-8 -*-

#modifies the script from http://babelfy.org/guide
import urllib2
import urllib
import json
import gzip

import csv
import nltk
import os

import sys
import getopt
from os import listdir
from os.path import isfile, join
from StringIO import StringIO
from SPARQLWrapper import SPARQLWrapper, JSON
from sets import Set

'''
PREFIX dbpedia: <http://dbpedia.org/resource/>
SELECT ?obj WHERE {
    dbpedia:Berlin (owl:sameAs|^owl:sameAs) ?obj
}
'''


def get_german_uri_from_english_dbpedia_uri(uri):
    '''
    Get a German URI via an English DBpedia URI.
    There are cases where multiple URIs are returned, but we only take the first one.
    :param uri: a DBpedia URI.
    :returns: German DBpedia URI
    '''
    #print "get city location using DBpedia uri"
    #here you have to decode the string first, not encode it
    #print uri
    res = 'nolink'
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery('''
        SELECT DISTINCT ?obj
        WHERE {
        <'''+urllib.unquote(uri).encode("utf8")+'''> (owl:sameAs|^owl:sameAs)* ?obj
        }
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results:
        for result in results["results"]["bindings"]:
            #print result
            if result["obj"]["value"].startswith('http://de.dbpedia.org/'):
                #print result["obj"]["value"]
                res = result["obj"]["value"]
            
    return res


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
        res = 'Other'
        sparql = SPARQLWrapper(lang)
        sparql.setQuery('''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
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
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Person', 'Http://xmlns.com/foaf/0.1/Person'):
                    res = 'Person'
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Place', 'http://dbpedia.org/ontology/Location', 'http://dbpedia.org/class/yago/YagoGeoEntity'):
                    res = 'Location'
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Organisation', 'http://dbpedia.org/class/yago/Organization108008335'):
                    res = 'Organisation'
        
        #print res
        return res

def babelnet(f, text, fileno, gitpath, tool):
    thefile = f
    service_url = 'https://babelfy.io/v1/disambiguate'
    results = gitpath + 'error_analysis/results/' + tool + "/" + dataset
    
    #text = 'BabelNet is both a multilingual encyclopedic dictionary and a semantic network'
    text = text
    lang = 'DE'
    key  = '2413d3ad-5c86-43f1-af71-656607dd14ee'
    annType = 'NAMED_ENTITIES'
    
    params = {
        'text' : text,
        'lang' : lang,
        'filterLangs': lang,
        'annType': annType,
        'key'  : key
    }
    
    url = service_url + '?' + urllib.urlencode(params)
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    
    #print "printing data"
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())
        
        print data    
        with open(results + dataset + "/" + fileno+'.json', 'w+') as resfile:
            json.dump(data, resfile)
        
        # retrieving data
        '''
        for result in data:
            # retrieving token fragment
            tokenFragment = result.get('tokenFragment')
            tfStart = tokenFragment.get('start')
            tfEnd = tokenFragment.get('end')
            #print str(tfStart) + "\t" + str(tfEnd)
    
            # retrieving char fragment
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')
            #print str(cfStart) + "\t" + str(cfEnd)
    
            # retrieving BabelSynset ID
            synsetId = result.get('babelSynsetID')
            dbpediaURL = result.get('DBpediaURL')
            #print synsetId
            #print dbpediaURL
            print thefile + "," + str(cfStart) + "," + str(cfEnd) + "," + dbpediaURL + ","
        '''
                 
def get_annotations(dataset, gitpath, tool):
    #'''
    #CREATES THE INITIAL RESULTS FILE - ENGLISH URIS
    mypath = gitpath + "/error_analysis/corpora/" + dataset + "/gold/" + dataset + "gold.csv"
    results = gitpath + "/error_analysis/results2/" + tool + "/" + dataset
    
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    
    for f in onlyfiles:
        #print f
        with open(os.path.join(mypath, f), 'rb') as textfile:
            current=textfile.read()
            text = current
            fileno = f.split('.')[0]
            print fileno
            #test(f)
            #print text
            babelnet(f, text, fileno)

def convert_annotations(folder, run, dataset, surface):
    results = folder + dataset
    print results
    onlyfiles2 = [ f for f in listdir(results) if isfile(join(results,f)) ]
    
    #data = ''
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
                    #german_url = get_german_uri_from_english_dbpedia_uri(rs['DBpediaURL'])
                    
                    #theType = get_dbpedia_type("http://dbpedia.org/sparql", rs['DBpediaURL'])
                    #theType = get_dbpedia_type("https://moses.semanticlab.net/fuseki/en.dbpedia.201510.1", rs['DBpediaURL'])
                    
                    done = 'a'
                    #if theType!='Other':
                    if done == 'a':
                        start = rs['charFragment']['start']
                        end = rs['charFragment']['end']+1
                        rdr = mypath + anno.split(".")[0] + ".txt"
                        #print rdr
                        #'''
                        sf = ''
                        with open(rdr, 'r') as reader:
                            data = reader.read().replace('\n', ' ')
                            #print data
                            sf = data[start:end]
                            #print sf
                        #print urllib.unquote(rs['DBpediaURL']).encode("utf8")
                        #'''
                        csvrun.write(anno.split(".")[0])
                        csvrun.write("|")
                        csvrun.write(str(rs['charFragment']['start']))
                        csvrun.write("|")
                        csvrun.write(str(rs['charFragment']['end']+1))
                        csvrun.write("|")
                        csvrun.write(urllib.unquote(rs['DBpediaURL']).encode("utf8"))
                        #csvrun.write(urllib.unquote(german_url).encode("utf8"))
                        csvrun.write("|")
                        csvrun.write("1")
                        csvrun.write("|")
                        #csvrun.write(theType)
                        csvrun.write(get_dbpedia_type("https://moses.semanticlab.net/fuseki/en.dbpedia.201510.1", rs['DBpediaURL']))
                        csvrun.write("|")
                        if surface==True:
                            csvrun.write(rs['surfaceForms'][0]['value'])
                            csvrun.write(sf)
                            csvrun.write("|")
                        csvrun.write("\n")
                        #'''
                        
                        '''    
                            if rs['key'] not in processed:
                                processed.add(rs['key'])
                                #print f.split("-")[0] + "|" + rs['key'] + "|" + rs['surfaceForms'][0]['value'] + "|" + str(rs['surfaceForms'][0]['startIndex']) + "|" +  str(rs['surfaceForms'][0]['endIndex']) + "|"
                                errw.write(f.split("-")[0] + "|")
                                errw.write(rs['key'].encode('utf-8') + "|")
                                errw.write(rs['surfaceForms'][0]['value'].encode('utf-8') + "|")
                                errw.write(str(rs['surfaceForms'][0]['startIndex']) + "|")
                                errw.write(str(rs['surfaceForms'][0]['endIndex']) + "|")
                                errw.write(" | |")
                                errw.write("\n")
                        '''
    print("end ca")
    
#if __name__ == '__main__':
    #print "start BABELNET evaluation"
    #get_annotations()
    #get_dbpedia_type("http://dbpedia.org/sparql", 'http://dbpedia.org/resource/Columbo')
    #convert_annotations(results, run)   
    #print "end"
    
    
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
        elif opt in ("-g", "--profile"):
            gitpath = arg
            
    print 'Path is: ', evalpath
    print 'Dataset is: ', dataset
    print 'Profile is:', profile
    print 'Gitpath is:', gitpath
    
    #get_annotations(dataset, gitpath, 'babelnet')
    
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