import requests
import requests_cache
from pathlib import Path
import habu.conf
import pickle
import shelve
from bs4 import BeautifulSoup
from pprint import pprint

db = shelve.open(habu.conf.workspace + '/db.shelve', writeback=True)

def analyze():

    if 'tech' not in db:
        db['tech'] = {}

    for r in db['requests']:
        host = r.request.url
        if 'Server' in r.headers:
            db['tech'][host] = { 'server': r.headers['Server'] }

    pprint(db['tech'])
    db.close()

if __name__ == '__main__':
    analyze()


