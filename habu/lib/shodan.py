#!/usr/bin/env python3

import logging
import os
import os.path

import requests
import requests_cache

from pathlib import Path

from habu.lib.loadcfg import loadcfg

config = loadcfg()

def shodan_get_result(ip, api_key=None, cache=True, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if cache:
        homedir = Path(os.path.expanduser('~'))
        requests_cache.install_cache(str(homedir / '.habu_requests_cache'), expire_after=3600)

    if not api_key:
        api_key = config['SHODAN_APIKEY']

    url = 'https://api.shodan.io/shodan/host/{}?key={}'.format(ip, api_key)

    r = requests.get(url)

    if r.status_code not in [200, 404]:
        logging.error(str(r))
        return {}

    if r.status_code == 404:
        return {}

    data = r.json()

    return data


def shodan_query(query, api_key, cache=True, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if cache:
        homedir = Path(os.path.expanduser('~'))
        requests_cache.install_cache(str(homedir / '.habu_requests_cache'), expire_after=3600)

    url = 'https://api.shodan.io/shodan/host/search?key={}&query={}'.format(api_key, query)

    r = requests.get(url)

    if r.status_code not in [200, 404]:
        logging.error(str(r))
        return {}

    if r.status_code == 404:
        return {}

    data = r.json()

    return data
