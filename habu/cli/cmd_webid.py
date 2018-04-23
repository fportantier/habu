import json
import os
import os.path
from pathlib import Path

import click

from habu.lib.webid import webid

@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
def cmd_webid(url, no_cache, verbose, output):
    response = webid(url, no_cache, verbose)
    output.write(json.dumps(response, indent=4))
    output.write('\n')

if __name__ == '__main__':
    cmd_webid()
