#!/usr/bin/env python3

import json
import logging
import os
import os.path
import pwd
import sys

import click
import requests
import requests_cache

from habu.lib.loadcfg import loadcfg


@click.command()
@click.argument('ip')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
def cmd_shodan(ip, no_cache, verbose, output):
    """Simple shodan API client with prints the json result of a shodan query

    Example:

    \b
    $ habu.shodan 8.8.8.8
    {
        "hostnames": [
            "google-public-dns-a.google.com"
        ],
        "country_code": "US",
        "org": "Google",
        "data": [
            {
                "isp": "Google",
                "transport": "udp",
                "data": "Recursion: enabled",
                "asn": "AS15169",
                "port": 53,
                "hostnames": [
                    "google-public-dns-a.google.com"
                ]
            }
        ],
        "ports": [
            53
        ]
    }
    """

    habucfg = loadcfg()

    if 'SHODAN_APIKEY' not in habucfg:
        print('You must provide a shodan apikey. Use the ~/.habu.json file (variable SHODAN_APIKEY), or export the variable HABU_SHODAN_APIKEY')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

    url = 'https://api.shodan.io/shodan/host/{}?key={}'.format(ip, habucfg['SHODAN_APIKEY'])

    r = requests.get(url)

    if r.status_code not in [200, 404]:
        print('ERROR', r)
        return False

    if r.status_code == 404:
        print("Not Found")
        return False

    data = r.json()

    output.write(json.dumps(data, indent=4))
    output.write('\n')

if __name__ == '__main__':
    cmd_shodan()
