import ipaddress
#from habu.lib.ip2asn import ip2asn
import json
import logging
import socket
import sys
import pwd
import os
from pprint import pprint

import click
import requests
import requests_cache
from bs4 import BeautifulSoup


def get_vhosts(ip, first=1, no_cache=False):
    """Returns a list of webs hosted on IP (checks bing.com)
    >>> 'www.bing.com' in vhosts(204.79.197.200)
    True
    """

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

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


@click.command()
@click.argument('host')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-p', 'pages', default=10, help='Pages count')
@click.option('-f', 'first', default=1, help='First result to get')
def cmd_vhosts(host, no_cache, pages, first):

    try:
        resolved = socket.gethostbyname(host)
    except Exception:
        logging.error('Invalid IP address or hostname')
        sys.exit(1)

    if host != resolved:
        print(host, '->', resolved, file=sys.stderr)

    vhosts = []

    for num in range(pages):
        #print("results", first+num*10)
        vhosts += get_vhosts(resolved, no_cache=no_cache, first=first+num*10)

    vhosts = list(set(vhosts))

    pprint(vhosts)

if __name__ == '__main__':
    cmd_vhosts()
