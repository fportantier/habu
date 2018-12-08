#!/usr/bin/env python3

import json
import logging
import socket

import click
import regex as re


def extract_hostname(data):

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

        result.add(candidate)

    return list(result)


@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-c', 'check', is_flag=True, default=False, help='Check if hostname resolves')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-j', 'jsonout', is_flag=True, default=False, help='JSON output')
def cmd_extract_hostname(infile, check, verbose, jsonout):
    """Extract hostnames from a file or stdin.

    Example:

    \b
    $ cat /var/log/some.log | habu.extract.hostname
    www.google.com
    ibm.com
    fileserver.redhat.com
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = extract_hostname(data)

    if check:
        logging.info('Checking against DNS...')
        for candidate in result:
            try:
                socket.getaddrinfo(candidate, None)
            except socket.gaierror:
                result.remove(candidate)

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_extract_hostname()
