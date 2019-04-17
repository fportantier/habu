#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.ip import geo_location


@click.command()
@click.argument('ip_address')
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
def cmd_ip_geolocation(ip_address, verbose):
    """Get the geolocation of an IP adddress from https://ipapi.co/.

    Example:

    \b
    $ habu.ip.geolocation 8.8.8.8
    {
        "ip": "8.8.8.8",
        "city": "Mountain View",
        ...
        "asn": "AS15169",
        "org": "Google LLC"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Looking up %s..." % ip_address, file=sys.stderr)

    results = geo_location(ip_address)

    if results:
        print(json.dumps(results, indent=4))
    else:
        print("[X] %s is not valid IPv4 address" % ip_address)

    return True


if __name__ == '__main__':
    cmd_ip_geolocation()
