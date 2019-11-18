import logging
import urllib.parse
from pathlib import Path

import regex as re
import requests
import requests_cache
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

def web_links(url, cache=True):
    """Returns all the links found in a web site"""

    if cache:
        requests_cache.install_cache(str(Path.home() / '.habu_requests_cache'), expire_after=3600)

    links = set()

    try:
        r = requests.get(url, timeout=5, verify=False)
    except Exception as e:
        return links

    soup = BeautifulSoup(r.content, 'lxml')

    http_url_regex = re.compile('http(s)?://', flags=re.IGNORECASE)

    for link in soup.findAll('a'):

        href = link.get('href')
        href = urllib.parse.urljoin(url, href)

        if not http_url_regex.match(href):
            continue

        links.add(href.rstrip('/'))


    for script in soup.findAll('script'):
        if 'src' not in script.attrs:
            continue

        file_url = urllib.parse.urljoin(url, script.attrs['src'])

        file_url = file_url.rstrip('/')
        links.add(file_url)


    for css in soup.findAll('link', attrs={'rel': 'stylesheet'}):

        file_url = css.attrs['href']
        file_url = urllib.parse.urljoin(url, file_url)

        file_url = file_url.rstrip('/')
        links.add(file_url)


    return links
