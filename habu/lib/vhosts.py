import os
from pathlib import Path

import requests
import requests_cache
from bs4 import BeautifulSoup


def get_vhosts(ip, first=1, no_cache=False):
    """Returns a list of webs hosted on IP (checks bing.com)
    >>> 'www.bing.com' in vhosts(204.79.197.200)
    True
    """

    if not no_cache:
        homedir = Path(os.path.expanduser('~'))
        requests_cache.install_cache((homedir / '.habu_requests_cache'), expire_after=3600)

    url = "http://www.bing.com/search?q=ip:{ip}&first={first}".format(ip=ip, first=first)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    vhosts = set()

    for h2 in soup.find_all('h2'):
        for link in h2.find_all('a'):
            href = link.get('href')

            if href.startswith('http://') or href.startswith('https://'):
                vhost = href.split('/')[2]
                vhosts.add(vhost)

    return list(vhosts)
