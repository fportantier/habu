#!/usr/bin/env python3

import ipaddress
import json
import logging

import click


@click.command()
@click.option('-i', 'infile', type=click.File('r'), default='-', help='Input file (Default: stdin)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--json', 'json_output', is_flag=True, default=False, help='JSON output')
@click.argument('field', type=click.STRING)
def cmd_data_select(infile, json_output, verbose, field):
    """Select a field from a JSON input.

    Example:

    \b
    $ cat /var/log/auth.log | habu.data.extract.ipv4 | habu.data.enrich | habu.data.filter cc eq US | habu.data.select asset
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

    if not isinstance(data, list):
        data = [data]

    for item in data:
        if field in item:
            result.append(item[field])

    if json_output:
        print(json.dumps(result, indent=4))
        return True

    for r in result:
        if isinstance(r, list):
            print('\n'.join(sorted(r)))
        else:
            print(r)


if __name__ == '__main__':
    cmd_data_select()
