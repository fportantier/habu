#!/usr/bin/env python3

import json
import warnings

import click
import whois


@click.command()
@click.argument('domain')
def cmd_whois_domain(domain):
    """Simple whois client to check domain names.

    Example:

    \b
    $ habu.whois.domain portantier.com
    {
        "domain_name": [
            "portantier.com"
        ],
        "registrar": "Amazon Registrar, Inc.",
        "whois_server": "whois.registrar.amazon.com",
        "referral_url": null,
        "updated_date": [
            "2018-05-12 21:58:24",
        ...
    """

    warnings.filterwarnings("ignore")
    data = whois.whois(domain)

    print(json.dumps(data, indent=4, default=str))

if __name__ == '__main__':
    cmd_whois_domain()
