#!/usr/bin/env python3

import ipaddress
import json
import logging
import sys

import click

from habu.lib.ip2asn import ip2asn


@click.command()
@click.argument('ip')
def cmd_ip2asn(ip):
    """Uses Team Cymru ip2asn service to get information about a public IPv4/IPv6.

    \b
    $ habu.ip2asn 8.8.8.8
    {
        "asn": "15169",
        "net": "8.8.8.0/24",
        "cc": "US",
        "rir": "ARIN",
        "asname": "GOOGLE - Google LLC, US",
        "country": "United States"
    }
    """

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        logging.error('Invalid IP address')
        sys.exit(1)

    data = ip2asn(ip)
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    cmd_ip2asn()
