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
def cmd_cymon_ip(ip, no_cache, verbose, output):
    """Simple cymon API client.

    Prints the JSON result of a cymon IP query.

    Example:

    \b
    $ habu.cymon.ip 8.8.8.8
    {
        "addr": "8.8.8.8",
        "created": "2015-03-23T12:03:42Z",
        "updated": "2018-08-24T04:06:07Z",
        "sources": [
            "safeweb.norton.com",
            "botscout.com",
            "virustotal.com",
            "phishtank"
        ],
        "events": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/events",
        "domains": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/domains",
        "urls": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/urls"
    }

    """

    habucfg = loadcfg()

    if 'CYMON_APIKEY' not in habucfg:
        print('You must provide a cymon apikey. Use the ~/.habu.json file (variable CYMON_APIKEY), or export the variable HABU_CYMON_APIKEY')
        print('Get your API key from https://www.cymon.io/')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

    url = 'https://www.cymon.io:443/api/nexus/v1/ip/{}'.format(ip)
    headers = { 'Authorization': 'Token {}'.format(habucfg['CYMON_APIKEY']) }

    r = requests.get(url, headers=headers)

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
    cmd_cymon_ip()
