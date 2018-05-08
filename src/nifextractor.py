#!/usr/bin/python
 # -*- coding: utf8 -*-
import urllib2
import json

import pandas
import urllib
import rdflib
import os
import sys

from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, FOAF, OWL, RDFS, XSD

from SPARQLWrapper import SPARQLWrapper, JSON
reload(sys)  
sys.setdefaultencoding('utf8')
#fix for encoding errors:
#http://www.markhneedham.com/blog/2015/05/21/python-unicodeencodeerror-ascii-codec-cant-encode-character-uxfc-in-position-11-ordinal-not-in-range128/


corpath = "/home/adrian/git/n3-collection/"

#kore50 = "/home/adrian/git/error_analysis/corpora/kore50/corpora/"
#kore50gold = "/home/adrian/git/error_analysis/corpora/kore50/gold/kore50.csv"

#reuters128 = "n3corpora/reuters128/Reuters-128.ttl"
#reuters128gold = "/home/adrian/git/error_analysis/corpora/reuters128/gold/reuters128gold-withsurface.csv"

#rss500 = "/home/adrian/git/error_analysis/corpora/rss500/corpora/"
#rss500gold = "/home/adrian/git/error_analysis/corpora/rss500/gold/rss500gold.csv"


#oke2015 = "/home/adrian/git/error_analysis/corpora/oke2015/corpora/"
#oke2015gold = "/home/adrian/git/error_analysis/corpora/oke2015/gold/oke2015gold.csv"

#oke2016 = "/home/adrian/git/error_analysis/corpora/oke2016/corpora/"
#oke2016gold = "/home/adrian/git/error_analysis/corpora/oke2016/gold/oke2016gold.csv"

#wes2015 = "/home/adrian/git/error_analysis/corpora/wes2015/corpora/"
#wes2015gold = "/home/adrian/git/error_analysis/corpora/wes2015/gold/wes2015gold.csv"

#news100 = "/home/adrian/git/error_analysis/corpora/news100/corpora/"
#news100gold = "/home/adrian/git/error_analysis/corpora/news100/gold/news100gold.csv"

rbb = "/home/adrian/git/error_analysis/corpora/rbb/corpora/"
rbbgold = "/home/adrian/git/error_analysis/corpora/rbb/gold/rbbgold.csv"

NIF = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
ITSRDF = Namespace("http://www.w3.org/2005/11/its/rdf#")
OKE = Namespace("http://www.ontologydesignpatterns.org/data/oke-challenge/task-1/")
DUL = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
DBPEDIA = Namespace("http://dbpedia.org/resource/")
D0 = Namespace("http://ontologydesignpatterns.org/ont/wikipedia/d0.owl#")
DC = Namespace("ttp://purl.org/dc/elements/1.1/")


def get_dbpedia_type(lang, uri):
        '''
        Get a German URI via an English DBpedia URI.
        There are cases where multiple URIs are returned, but we only take the first one.
        :param uri: a DBpedia URI.
        :returns: a DBpedia type
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
                #print result
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Place', 'http://dbpedia.org/ontology/Location', 'http://dbpedia.org/class/yago/YagoGeoEntity'):
                    res = 'Place'
                if result["obj"]["value"] in ('http://dbpedia.org/ontology/Person', 'http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/class/yago/Person100007846', 'http://dbpedia.org/class/yago/FictionalCharacter109587565','http://dbpedia.org/class/yago/SpiritualBeing109504135'):
                    res = 'Person'
                if result["obj"]["value"] in ('http://extract_files_from_nif_corpus("oke2015.ttl", oke2015)dbpedia.org/ontology/Organisation', 'http://dbpedia.org/class/yago/Organization108008335', 'http://dbpedia.org/class/yago/Group100031264'):
                    res = 'Organization'
            
        return res


def extract_files_from_nif_corpus(corpus, folder, urlsplitter):
    """
    Extracts the documents from a NIF corpus/corpora.
    :param corpus: the corpus filename
    :param folder: the ouput folder for the corpus
    :returns: -
    """
    g = Graph()
    g.parse(corpath + corpus, format="turtle")
    print len(g) 
    
    for s,p,o in g.triples((None, NIF.isString, None)):
        #print s
        #5 previously
        docno = (s.split("/")[urlsplitter]).split("#")[0]
        print docno
        print o
        filename = folder + docno + ".txt"
        #if not os.path.exists(filename):
        if not os.path.exists(filename):
            target = open(filename,  'w+')
            target.write(o.encode('utf-8'))
            target.close()

def extract_entities_from_nif_corpus(corpus, gold, urlsplitter):
    g = Graph()
    g.parse(corpath + corpus, format="turtle")
    #print len(g)
    
    fh = open(gold,'w')
    
    ts = 0
    for s,p,o in g.triples((None, NIF.anchorOf, None)):
        #5 for N3-collection
        #8 for kore50
        #6 for oke
        #7 for wes
        docsplit = (s.split("/")[urlsplitter]).split("#")
        docno = docsplit[0]
        #print docno
        surfaceForm = o
        
        print docsplit
        commaSplit = docsplit[1].split(",")
        start = commaSplit[0].split("=")[1]
        end = commaSplit[1]
        
        #print docno, surfaceForm, start, end
        
        s2 = s

        for s2,p2,o2 in g.triples((s2, ITSRDF.taIdentRef, None)):
        #for s2,p2,o2 in g.triples((s2, OWL.sameAs, None)):
            #link = o2
            #print link
            #print docno, surfaceForm, start, end, link
            link = o2
            if docno!="365":
                type = get_dbpedia_type('http://de.dbpedia.org/sparql', link)
            else:
                type = "notype"
            #print type
                
            #print docno + "|" +  start + "|" + end + ", " + surfaceForm + ", " + link + ","
            print docno + "|" +  start + "|" + end + "|" + link + "|1|" + type + "|"
                
            #fh.write(docno + "|" +  start + "|" + end + "|" + link.encode('utf-8').strip() + "|1|" + type + "|")
            fh.write(docno + "|" +  start + "|" + end + "|" + link.encode('utf-8').strip() + "|1|" + type + "|"+ surfaceForm + "|")
            #+ urllib.unquote(link).decode("utf8") + ", "
            fh.write('\n')
            
            '''
            #this is only for WES
            s3 = o2
            for s3,p3,o3 in g.triples((s3, OWL.sameAs, None)):
                print o3
                link = o3
                if docno!="265":
                    type = get_dbpedia_type('http://dbpedia.org/sparql', link)
                else:
                    type = "notype"
                print type
                
                #print docno + "|" +  start + "|" + end + ", " + surfaceForm + ", " + link + ","
                print docno + "|" +  start + "|" + end + "|" + link + "|1|" + type + "|"
                
                #fh.write(docno + "|" +  start + "|" + end + "|" + link.encode('utf-8').strip() + "|1|" + type + "|")
                fh.write(docno + "|" +  start + "|" + end + "|" + link.encode('utf-8').strip() + "|1|" + type + "|"+ surfaceForm + "|")
                #+ urllib.unquote(link).decode("utf8") + ", "
                fh.write('\n')
            '''
            
    fh.close()
        
                       
    

if __name__ == '__main__':
    print "start"
    
    #ENGLISH DATASETS
    #extract_files_from_nif_corpus("RSS-500.ttl", rss500)
    #extract_entities_from_nif_corpus("RSS-500.ttl", rss500gold)

    #extract_files_from_nif_corpus("kore50.ttl", kore50)
    #extract_entities_from_nif_corpus("kore50.ttl", kore50gold)

    #extract_files_from_nif_corpus("oke2015.ttl", oke2015)
    #extract_entities_from_nif_corpus("oke2015.ttl", oke2015gold)
    
    #extract_files_from_nif_corpus("oke2016.ttl", oke2016)
    #extract_entities_from_nif_corpus("oke2016.ttl", oke2016gold)
     
    #extract_files_from_nif_corpus("wes2015.ttl", wes2015)
    #extract_entities_from_nif_corpus("wes2015.ttl", wes2015gold)

    #extract_files_from_nif_corpus("Reuters-128.ttl", reuters128)
    #extract_entities_from_nif_corpus("Reuters-128.ttl", reuters128gold)
    
   
    #GERMAN DATASETS
    #extract_files_from_nif_corpus("News-100.ttl", news100, 5)
    #extract_entities_from_nif_corpus("News-100.ttl", news100gold, 5)
    
    #extract_files_from_nif_corpus("rbb.ttl", rbb, 3)
    extract_entities_from_nif_corpus("rbb.ttl", rbbgold, 3)

    print "end"