#!/usr/bin/env python3

import json
import warnings

import click
from ipwhois import IPWhois


@click.command()
@click.argument('ip')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
@click.option('--csv', 'csv_output', is_flag=True, default=False, help='Print the output in CSV format')
def cmd_whois_ip(ip, json_output, csv_output):
    """Simple whois client to check IP addresses (IPv4 and IPv6).

    Example:

    \b
    $ habu.whois.ip 8.8.4.4
    asn                      15169
    asn_registry             arin
    asn_cidr                 8.8.4.0/24
    asn_country_code         US
    asn_description          GOOGLE - Google LLC, US
    asn_date                 1992-12-01
    """

    warnings.filterwarnings("ignore")

    default_fields = [
        'asn',
        'asn_registry',
        'asn_cidr',
        'asn_country_code',
        'asn_description',
        'asn_date',
    ]

    obj = IPWhois(ip)
    data = obj.lookup_rdap()

    if json_output:
        print(json.dumps(data, indent=4))
        return True

    for field in default_fields:
        value = data.get(field, None)
        if not field:
            continue

        if csv_output:
            print('"{}","whois.{}","{}"'.format(ip, field, value))
        else:
            print('{:<25}{}'.format(field, value))


if __name__ == '__main__':
    cmd_whois_ip()
