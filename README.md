# crawldns
a simple python script for doing a small pentest utility that make use of the CommonCrawl data set API 

# Usage:
- running the tool:

- python CCrawlDNS.py -d example.com

- python3 CCrawlDNS.py -d example.com

- Print all URLs:

- python CCrawlDNS.py -d example.com -p

- Print all URLs with the file extension ".asp":

- python CCrawlDNS.py -d example.com -p -f .asp

# Requirements:

- pip install requests