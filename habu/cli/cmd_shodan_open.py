#!/usr/bin/env python3

import json
import logging
import os
import os.path
import pwd
import sys

import click

from habu.lib.loadcfg import loadcfg
from habu.lib.shodan import shodan_get_result

@click.command()
@click.argument('ip')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-j', 'json_output', is_flag=True, default=False, help='Output in JSON format')
@click.option('-x', 'nmap_command', is_flag=True, default=False, help='Output an nmap command to scan open ports')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
def cmd_shodan_open(ip, no_cache, json_output, nmap_command, verbose, output):
    """Output the open ports for an IP against shodan (nmap format).

    Example:

    \b
    $ habu.shodan.open 8.8.8.8
    T:53,U:53
    """

    habucfg = loadcfg()

    if 'SHODAN_APIKEY' not in habucfg:
        print('You must provide a shodan apikey. Use the ~/.habu.json file (variable SHODAN_APIKEY), or export the variable HABU_SHODAN_APIKEY')
        print('Get your API key from https://www.shodan.io/')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = shodan_get_result(ip, habucfg['SHODAN_APIKEY'], no_cache, verbose)
    ports = []

    if 'data' in data:
        for service in data['data']:
            ports.append('{}:{}'.format(
                service['transport'][0].upper(),
                service['port']
            ))

    if nmap_command:
        if ports:
            output.write('nmap -A -v -p {} {}'.format(','.join(ports), ip))
    else:
        if json_output:
            output.write(json.dumps(ports, indent=4))
            output.write('\n')
        else:
            output.write(','.join(ports))

if __name__ == '__main__':
    cmd_shodan_open()
