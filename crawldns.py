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

def GetLinks(CdxApi, IndexNum):
    	print("Processing {0}".format(IndexNum))
	Req = requests.get(CdxApi+'?url='+Target+'&fl=url&matchType=domain&pageSize=2000&output=json')
	Ans = Req.text.split('\n')[:-1]
	try:
		for entry in Ans:
			Url = json.loads(entry)['url']
			if PrintURL is True and FileExt is not None:
				URLZ = re.findall(FileExt, Url)
				if URLZ:
					print(Url)
			if PrintURL is True and FileExt is None:
				print(Url)

			Domains =  re.findall(r'(?<=://)[^/|?|#]*', Url)[0]
			SaveSubDomainToDb({
					'Domain': Domains
					})
		print("{0} Processed".format(IndexNum))
	except:
		pass

def GetIndexFile():
	IndexURL = "https://index.commoncrawl.org/collinfo.json"
	Data = requests.get(IndexURL).text
	Indexes = json.loads(Data)
	threads = []
	print("You have %s CPUs...\nLet's use them all!"%multiprocessing.cpu_count())
	Pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
	for res in Indexes:
		proc = Pool.apply_async(GetLinks, (res['cdx-api'],(res['id'])))
		threads.append(proc)
	for proc in threads:
		proc.get()

def main():
    CreatePentestDb()
    cursor = DbConnect()
    GetIndexFile()
    GetSubdomainStatistic(cusor)
    GetSubdomains(cursor)

if __name__ == '__main__':
    main()
    

