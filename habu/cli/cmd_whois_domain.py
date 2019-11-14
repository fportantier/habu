#!/usr/bin/env python3

import json
import warnings

import click
import whois


def remove_duplicates(data):
    for key in data.keys():
        if isinstance(data[key], list):
            if hasattr(data[key][0], 'lower'):
                data[key] = list(set([ item.lower() for item in data[key] ]))
            else:
                data[key] = data[key][0]

    if isinstance(data['domain_name'], list):
        data['domain_name'] = data['domain_name'][0]

    return data


@click.command()
@click.argument('domain')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
@click.option('--csv', 'csv_output', is_flag=True, default=False, help='Print the output in CSV format')
def cmd_whois_domain(domain, json_output, csv_output):
    """Simple whois client to check domain names.

    Example:

    \b
    $ habu.whois.domain google.com
    registrar                MarkMonitor, Inc.
    whois_server             whois.markmonitor.com
    creation_date            1997-09-15 04:00:00
    expiration_date          2028-09-14 04:00:00
    name_servers             ns1.google.com, ns2.google.com, ns3.google.com, ns4.google.com
    emails                   abusecomplaints@markmonitor.com, whoisrequest@markmonitor.com
    dnssec                   unsigned
    org                      Google LLC
    country                  US
    state                    CA
    """

    default_fields = [
        'registrar',
        'whois_server',
        'update_date',
        'creation_date',
        'expiration_date',
        'name_servers',
        'emails',
        'dnssec',
        'org',
        'country',
        'state',
        'city',
        'address',
    ]


    warnings.filterwarnings("ignore")

    data = whois.whois(domain)
    data = remove_duplicates(data)

    if json_output:
        print(json.dumps(data, indent=4, default=str))
        return True

    for field in default_fields:
        value = data.get(field, None)
        if not value:
            continue

        if csv_output:
            if not isinstance(value, list):
                value = [value]
            for v in sorted(value):
                print('"{}","whois.{}","{}"'.format(domain, field, v))
        else:
            if isinstance(value, list):
                value = ', '.join(sorted(value))
            print('{:<25}{}'.format(field, value))


if __name__ == '__main__':
    cmd_whois_domain()
