import json
import logging
import os.path
import sys
from pathlib import Path
from pprint import pprint

import click
import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup


def extract_ip(data):

    regexp = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', flags=re.MULTILINE)

    match = regexp.finditer(data)

    result = []
    for m in match:
        result.append(m.group(0))

    return result

supported = [
    'ip',
]

@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-j', 'jsonout', is_flag=True, default=False, help='JSON output')
@click.option('-w', 'what', default='ip', type=click.Choice(supported), help='What do you want to extract')
def cmd_extract(infile, verbose, jsonout, what):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = []

    functions = {
        'ip' : [ extract_ip ]
    }

    for f in functions[what]:
        #print(f)
        result += f(data)

    result = sorted(set(result))

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_extract()
