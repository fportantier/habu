#!/usr/bin/env python3

import ipaddress
import json
import logging

import click


@click.command()
@click.option('-i', 'infile', type=click.File('r'), default='-', help='Input file (Default: stdin)')
@click.option('-j', 'json_output', is_flag=True, default=False, help='JSON output')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.argument('field', type=click.STRING)
def cmd_select(infile, json_output, verbose, field):
    """Select a field from a JSON input.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.ipv4 | habu.expand | habu.filter cc eq US | habu.select asset
    8.8.8.7
    8.8.8.8
    8.8.8.9
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        data = json.loads(infile.read())
    except ValueError as e:
        print(e)
        click.echo('Invalid input data. Whe expect JSON here.', err=True)
        return False

    result = []

    for item in data:
        if field in item:
            result.append(item[field])

    if json_output:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_select()
