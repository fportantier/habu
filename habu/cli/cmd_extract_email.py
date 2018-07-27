#!/usr/bin/env python3

import json
import logging

import click
import regex as re


def extract_email(data):

    regexp = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

    match = regexp.finditer(data)

    result = []

    for m in match:
        result.append(m.group(0))

    return result


@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-j', 'jsonout', is_flag=True, default=False, help='JSON output')
def cmd_extract_email(infile, verbose, jsonout):
    """Extract email addresses from a file or stdin.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.email
    john@securetia.com
    raven@acmecorp.net
    nmarks@fimax.com
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = []

    result = extract_email(data)

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_extract_email()
