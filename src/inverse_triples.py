#!/usr/bin/python
# -*- coding: utf-8 -*-
import rdflib
from rdflib import ConjunctiveGraph, URIRef,RDF, OWL, Literal

print("start")
g = rdflib.Graph()
g2 = rdflib.Graph()
g.parse("/home/adrian/data/links/wikidata_en.ttl", format="turtle")

print("graph was parsed")

for s,p,o in g:
    #print s,p,o
    g2.add((o, p, s))
print("end loop")

g2.serialize("/home/adrian/data/links/wikidata_dbp_en.ttl", format="turtle")
    
print("end")