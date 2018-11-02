#!/usr/bin/env python3

import json
import warnings

import click
from ipwhois import IPWhois


@click.command()
@click.argument('ip')
def cmd_whois_ip(ip):
    """Simple whois client to check IP addresses (IPv4 and IPv6).

    Example:

    \b
    $ habu.whois.ip 8.8.8.8
    {
        "nir": null,
        "asn_registry": "arin",
        "asn": "15169",
        "asn_cidr": "8.8.8.0/24",
        "asn_country_code": "US",
        "asn_date": "1992-12-01",
        "asn_description": "GOOGLE - Google LLC, US",
        "query": "8.8.8.8",
        ...
    """

    warnings.filterwarnings("ignore")

    obj = IPWhois(ip)
    data = obj.lookup_rdap()

    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    cmd_whois_ip()
