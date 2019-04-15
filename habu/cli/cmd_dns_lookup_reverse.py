"""Perform a reverse lookup of an IP address."""
import json
import logging
import sys

import click

from habu.lib.dns import lookup_reverse


@click.command()
@click.argument('ip_address')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dns_lookup_reverse(ip_address, verbose):
    """Perform a reverse lookup of a given IP address.

    Example:

    \b
    $ $ habu.dns.lookup.reverse 8.8.8.8
    {
        "hostname": "google-public-dns-a.google.com"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Looking up %s..." % ip_address, file=sys.stderr)

    answer = lookup_reverse(ip_address)

    if answer:
        print(json.dumps(answer, indent=4))
    else:
        print("[X] %s is not valid IPv4/IPV6 address" % ip_address)

    return True


if __name__ == '__main__':
    cmd_dns_lookup_reverse()
