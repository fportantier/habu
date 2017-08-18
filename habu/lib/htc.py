import requests
import requests_cache
from pathlib import Path
import habu.conf
import pickle
import shelve
from bs4 import BeautifulSoup
from pprint import pprint

db = shelve.open(habu.conf.workspace + '/db.shelve', writeback=True)
requests_cache.install_cache(habu.conf.workspace + '/requests_cache')

if not 'requests' in db:
    print('crea')
    db['requests'] = []


def get_urls_from_response(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a')]
    return set(urls)


def crawl(url):
    root = url
    s = requests.Session()
    visited = set()
    to_visit = set([url])

    while True:
        try:
            url = to_visit.pop()
        except KeyError:
            break

        print('GET ', url)

        try:
            visited.add(url)

            r = s.get(url)
            if not r.from_cache:
                db['requests'].append(r)

            print(r.headers)

        except requests.exceptions.MissingSchema:
            continue

        for u in get_urls_from_response(r):
            if u.startswith(root) and u not in visited:
                to_visit.add(u)

    db.close()


if __name__ == '__main__':
    crawl('http://spds.info/')


