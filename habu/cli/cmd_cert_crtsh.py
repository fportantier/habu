#!/usr/bin/env python3

import json
import logging
import os
import os.path
import sys

from pathlib import Path

import click
import requests
import requests_cache

from habu.lib.dnsx import query_bulk

@click.command()
@click.argument('domain')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-n', 'no_validate', is_flag=True, default=False, help='Disable DNS subdomain validation')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
def cmd_cert_crtsh(domain, no_cache, no_validate, verbose, json_output):
    """Downloads the certificate transparency logs for a domain
    and check with DNS queries if each subdomain exists.

    Uses multithreading to improve the performance of the DNS queries.

    Example:

    \b
    $ habu.crtsh securetia.com
    alt.securetia.com
    other.securetia.com
    www.securetia.com
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = Path(os.path.expanduser('~'))
        requests_cache.install_cache(str((homedir / '.habu_requests_cache')), expire_after=3600)

    subdomains = set()

    if verbose:
        print("Downloading subdomain list from https://crt.sh ...", file=sys.stderr)

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=domain))

    if req.status_code != 200:
        print("[X] Information not available!")
        exit(1)

    json_data = json.loads(req.text)

    for data in json_data:
        name = data['name_value'].lower()
        if '*' not in name:
            subdomains.add(name)

    subdomains = list(subdomains)

    if not no_validate:
        if verbose:
            print("Validating subdomains against DNS servers ...", file=sys.stderr)

        answers = query_bulk(subdomains)

        validated = []

        for answer in answers:
            if answer:
                validated.append(str(answer.qname))

        subdomains = validated

    if json_output:
        print(json.dumps(sorted(subdomains), indent=4))
    else:
        print('\n'.join(sorted(subdomains)))

    return True



if __name__ == '__main__':
    cmd_cert_crtsh()
