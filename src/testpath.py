#!/usr/bin/python3
# -*- coding: utf-8 -*

import sys, os


#print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])        
#print('path =', pathname)
#abspath should be used instead of realpath to make sure it works in any os
print('full path =', os.path.abspath(pathname)) 

path = os.path.normpath(pathname)
splitpath = path.split(os.sep)
gitbase = (os.sep).join(splitpath[:len(splitpath)-2])

#print >>sys.stderr, "gitbase"
print(gitbase)