#!/usr/bin/env python3

import json
import warnings

import click

# next lines because the pypi package python-whois uses the namespace 'whois' and
# the Debian python3-pywhois uses the namespace 'pywhois' at least on 2018-11-03
try:
    import pywhois as whois
except ModuleNotFoundError:
    import whois


def remove_duplicates(data):
    for key in data.keys():
        if type(data[key]) == type([]):
            if hasattr(data[key][0], 'lower'):
                data[key] = list(set([ item.lower() for item in data[key] ]))
            else:
                data[key] = data[key][0]

    if type(data['domain_name']) == type([]):
        data['domain_name'] = data['domain_name'][0]

    return data


@click.command()
@click.argument('domain')
def cmd_whois_domain(domain):
    """Simple whois client to check domain names.

    Example:

    \b
    $ habu.whois.domain portantier.com
    {
        "domain_name": "portantier.com",
        "registrar": "Amazon Registrar, Inc.",
        "whois_server": "whois.registrar.amazon.com",
        ...
    """

    warnings.filterwarnings("ignore")

    data = whois.whois(domain)
    data = remove_duplicates(data)

    print(json.dumps(data, indent=4, default=str))

if __name__ == '__main__':
    cmd_whois_domain()
