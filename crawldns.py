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

def CreatePentestDb():
    if os.path.exists('./Results.db'):
        cursor = DbConnect()
        cursor.execute('DROP TABLE SubDomain')
        cursor.commit()
        cursor.close()
    if not os.path.exists('./Results.db'):
        cursor = DbConnect()
        cursor.execute('CREATE TABLE SubDomain (timestamp TEXT, Domain TEXT, Links Text)')
        cursor.commit()
        cursor.close()

def SaveSubDomainToDb(result):
    	for k in [ 'timestamp', 'Domain', 'Links']:
		if not k in result:
			result[k] = ''
	cursor = DbConnect()
	cursor.text_factory = sqlite3.Binary
	res = cursor.execute("SELECT COUNT(*) AS count FROM SubDomain WHERE Domain=? AND Links=?", (result['Domain'], result['Links']))
	(count,) = res.fetchone()
	if not count:
		cursor.execute("INSERT INTO SubDomain VALUES(datetime('now'), ?, ?)", (result['Domain'], result['Links']))
		cursor.commit()
	cursor.close()

def GetSubdomainStatistic(cursor):
     res = cursor.execute("SELECT COUNT(DISTINCT UPPER(Domain)) FROM SubDomain")
     for row in res.fetchall():
         print('\n[+] In total {0} unique subdomains were retrieved.'.format(row[0]))

def GetSubdomains(cursor):
     res = cursor.execute("SELECT DISTINCT Domain FROM SubDomain")
     for row in res.fetchall():
         print('Subdomain found: {0}'.format(row[0]))

