#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.http import get_options


@click.command()
@click.argument('server')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_http_options(server, verbose):
    """Retrieve the available HTTP methods of a web server.

    Example:

    \b
    $ habu.http.options -v http://google.com
    {
        "allowed": "GET, HEAD"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if verbose:
        print("[-] Retrieving the HTTP headers of the server...")

    options = get_options(server)

    if type(options) is dict:
        print(json.dumps(options, indent=4))
        if verbose:
            print("[+] HTTP options from {} retrieved".format(server))
    else:
        print("[X] {}".format(options), file=sys.stderr)

    return True


if __name__ == '__main__':
    cmd_http_options()

