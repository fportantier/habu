#!/usr/bin/env python3

import json
import logging
import sys

import click
import requests


def karma(ip):
    URL = 'https://karma.securetia.com/api/ip/'
    r = requests.get(URL + ip, headers={'Accept': 'application/json'})

    if r.status_code != 200:
        logging.error('HTTP Error code received: {}'.format(r.status_code))
        sys.exit(1)

    return r.json()


@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('--json', 'jsonout', is_flag=True, default=False, help='JSON output')
@click.option('--bad', 'badonly', is_flag=True, default=False, help='Show only entries in blacklists')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_karma_bulk(infile, jsonout, badonly, verbose):
    """Show which IP addresses are inside blacklists using the Karma online service.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.ipv4 | habu.karma.bulk
    172.217.162.4   spamhaus_drop,alienvault_spamming
    23.52.213.96    CLEAN
    190.210.43.70   alienvault_malicious
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = {}

    for ip in data.split('\n'):
        if ip:
            logging.info('Checking ' + ip)
            response = karma(ip)
            if response:
                result[ip] = response
            elif not badonly:
                result[ip] = ['CLEAN']

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        for k,v in result.items():
            print(k, '\t', ','.join(v))


if __name__ == '__main__':
    cmd_karma_bulk()
