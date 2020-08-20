#!/usr/bin/env python3

import ipaddress
import json
import logging
import os
import sys

import click

from habu.lib import dnsx

from habu.lib.loadcfg import loadcfg
from habu.lib.shodan import shodan_get_result

@click.command()
@click.argument('ip')
@click.option('--cache/--no-cache', 'cache', default=True)
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--format', 'output_format', type=click.Choice(['txt', 'csv','json', 'nmap']), default='txt', help='Output format')
def cmd_shodan(ip, cache, verbose, output_format):
    """Simple shodan API client.

    Prints the JSON result of a shodan query.

    Example:

    \b
    $ habu.shodan 216.58.222.36
    asn                      AS15169
    isp                      Google
    hostnames                eze04s06-in-f4.1e100.net, gru09s17-in-f36.1e100.net
    country_code             US
    region_code              CA
    city                     Mountain View
    org                      Google
    open_ports               tcp/443, tcp/80
    """

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        ip = dnsx.resolve(ip)

    if ip and isinstance(ip, list):
        ip = ip[0]
        logging.info('Resolved to {}'.format(ip))

    if not ip:
        logging.error('Invalid IP address or unresolvable name')
        return False

    habucfg = loadcfg()

    if 'SHODAN_APIKEY' not in habucfg:
        print('You must provide a shodan apikey. Use the ~/.habu.json file (variable SHODAN_APIKEY), or export the variable HABU_SHODAN_APIKEY')
        print('Get your API key from https://www.shodan.io/')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = shodan_get_result(ip, habucfg['SHODAN_APIKEY'], cache=cache, verbose=verbose)

    if output_format == 'json':
        print(json.dumps(data, indent=4))
        return True

    if not data:
        logging.error('Shodan seems to have no data for this host')
        return False

    if output_format == 'nmap':
        ports_string = ','.join(['{}:{}'.format(port['transport'][0].upper(), port['port']) for port in data['data']])
        print(ports_string, end='')
        return True

    default_fields = [
        'asn',
        'isp',
        'hostnames',
        'country_code',
        'region_code',
        'city',
        'org',
        'os',
    ]

    for field in default_fields:
        value = data.get(field, None)
        if not value:
            continue

        if output_format == 'csv':
            if not isinstance(value, list):
                value = [value]
            for v in sorted(value):
                print('"{}","shodan.{}","{}"'.format(ip, field, v))
        else:
            if isinstance(value, list):
                value = ', '.join(sorted(value))
            print('{:<25}{}'.format(field, value))

    if output_format == 'txt':
        ports_string = ', '.join(['{}/{}'.format(port['transport'], port['port']) for port in data['data']])
        print('{:<25}{}'.format('open_ports', ports_string))
    else:
        for port in data['data']:
            print('"{}","shodan.open_port","{}/{}"'.format(ip, port['transport'], port['port']))


if __name__ == '__main__':
    cmd_shodan()
