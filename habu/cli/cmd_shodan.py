#!/usr/bin/env python3

import json
import logging
import os
import sys

import click

from habu.lib.loadcfg import loadcfg
from habu.lib.shodan import shodan_get_result

@click.command()
@click.argument('ip')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
def cmd_shodan(ip, no_cache, verbose, output):
    """Simple shodan API client.

    Prints the JSON result of a shodan query.

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
        print('Get your API key from https://www.shodan.io/')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = shodan_get_result(ip, habucfg['SHODAN_APIKEY'], no_cache, verbose)

    output.write(json.dumps(data, indent=4))
    output.write('\n')

if __name__ == '__main__':
    cmd_shodan()
