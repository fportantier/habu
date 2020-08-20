#!/usr/bin/env python3

import json
import logging
import socket
import tldextract

import click
import regex as re

from habu.lib import dnsx


def extract_domain(data):

    regexp = re.compile(r"([a-zA-Z0-9_.-]+)")

    match = regexp.finditer(data)

    result = set()

    for m in match:

        candidate = m.group(0).lower()

        if '.' not in candidate:
            continue

        if not re.match('[a-z]+', candidate):
            continue

        if not re.match('[a-z0-9]+\.[a-z0-9]', candidate):
            continue

        tld = tldextract.extract(candidate)
        if tld.suffix:
            result.add(tld.domain + '.' + tld.suffix.rstrip('.'))

    return list(result)


@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-c', 'check', is_flag=True, default=False, help='Check if domain has NS servers defined')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-j', 'jsonout', is_flag=True, default=False, help='JSON output')
def cmd_data_extract_domain(infile, check, verbose, jsonout):
    """Extract valid domains from a file or stdin.

    Optionally, check each domain for the presence of NS registers.

    Example:

    \b
    $ cat /var/log/some.log | habu.data.extract.domain -c
    google.com
    ibm.com
    redhat.com
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = extract_domain(data)

    if check:
        logging.info('Checking against DNS...')
        result = [ domain for domain in result if dnsx.ns(domain) ]

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_data_extract_domain()
