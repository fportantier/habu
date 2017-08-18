import requests
import os
import csv
import operator
from pprint import pprint

url_nmap_services = 'https://svn.nmap.org/nmap/nmap-services'

FILEDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
SERVICES_FILE = os.path.abspath(os.path.join(DATADIR, 'services'))

def update_nmap_services():

    services = []

    r = requests.get(url_nmap_services)

    if r.status_code != 200:
        return None

    for line in r.text.split('\n'):

        if line.startswith('#'):
            continue

        l = line.split('\t', maxsplit=3)

        if len(l) > 2:
            services.append(l)

    for protocol in ['tcp', 'udp']:
        with open(SERVICES_FILE + '-' + protocol, 'w') as output:
            for row in sorted(services, reverse=True, key=operator.itemgetter(2)):
                if protocol in row[1]:
                    output.write("%s\n" %(row[1].split('/')[0]))

if __name__ == '__main__':
    update_nmap_services()

