#!/usr/bin/env python3

import logging
import os
import os.path
import pwd

import requests
import requests_cache


def shodan_get_result(ip, api_key, no_cache=False, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

    url = 'https://api.shodan.io/shodan/host/{}?key={}'.format(ip, api_key)

    r = requests.get(url)

    if r.status_code not in [200, 404]:
        logging.error(str(r))
        return {}

    if r.status_code == 404:
        return {}

    data = r.json()

    return data
