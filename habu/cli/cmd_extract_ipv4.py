#!/usr/bin/env python3

import json
import logging

import click
import regex as re


def extract_ipv4(data):

    regexp = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', flags=re.MULTILINE)

    match = regexp.finditer(data)

    result = []

    for m in match:
        result.append(m.group(0))

    return result

@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-j', '--json', 'json_output', is_flag=True, default=False, help='JSON output')
@click.option('-u', '--unique', 'unique', is_flag=True, default=False, help='Remove duplicates')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_extract_ipv4(infile, json_output, unique, verbose):
    """Extract IPv4 addresses from a file or stdin.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.ipv4
    172.217.162.4
    23.52.213.96
    190.210.43.70
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = []

    result = extract_ipv4(data)

    if unique:
        result = list(set(result))

    if not json_output:
        print('\n'.join(result))
        return True

    result_dict = [ { 'ipv4_address' : ip } for ip in result ]
    print(json.dumps(result_dict, indent=4))

if __name__ == '__main__':
    cmd_extract_ipv4()
