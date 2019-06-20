#!/usr/bin/env python3

import json
import logging

import click

from habu.lib.expand import expand


@click.command()
@click.option('-i', 'infile', type=click.File('r'), default='-', help='Input file (Default: stdin)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_expand(infile, verbose):
    """Expand data to add interesting information.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.ipv4 | habu.expand
    [
        {
            "asset": "8.8.8.8",
            "family": "IPAddress",
            "asn": "15169",
            "net": "8.8.8.0/24",
            "cc": "US",
            "rir": "ARIN",
            "asname": "GOOGLE - Google LLC, US"
        },
        {
            "asset": "8.8.4.4",
            "family": "IPAddress",
            "asn": "15169",
            "net": "8.8.4.0/24",
            "cc": "US",
            "rir": "ARIN",
            "asname": "GOOGLE - Google LLC, US"
        }
    ]
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    lines = infile.read().split('\n')

    result = [ expand(line) for line in lines if line ]

    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    cmd_expand()
