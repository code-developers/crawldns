#!/usr/bin/env/python

#imports
import requests
import json
import optparse
import re
import os
import sys
import multiprocessing
import sqlite3

parser = optparse.OptionParser(usage='python %prog -p -f asp -d microsoft.com', prog=sys.argv[0])
parser.add_option('-d','--domain', action="store", help="Target domain", dest="Domain", default=None)
parser.add_option('-p','--printurl', action="store_true", help="Print all collected URL", dest="PrintURL", default=None)
parser.add_option('-f','--FileExt', action="store", help="Print collected URL with the following file extension", dest="FileExt", default=None)
options, args = parser.parse_args()
Target = options.Domain
PrintURL = options.PrintURL
FileExt = options.FileExt

if Target is None:
    sys.exit('Mandatory option -d missing..\nExiting..')

def DbConnect():
    cursor = sqlite3.connect('./Result.db')
    return cursor
