#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.http import get_headers


@click.command()
@click.argument('server')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_http_headers(server, verbose):
    """Retrieve the HTTP headers of a web server.

    Example:

    \b
    $ habu.http.headers http://duckduckgo.com
    {
        "Server": "nginx",
        "Date": "Sun, 14 Apr 2019 00:00:55 GMT",
        "Content-Type": "text/html",
        "Content-Length": "178",
        "Connection": "keep-alive",
        "Location": "https://duckduckgo.com/",
        "X-Frame-Options": "SAMEORIGIN",
        "Content-Security-Policy": "default-src https: blob: data: 'unsafe-inline' 'unsafe-eval'",
        "X-XSS-Protection": "1;mode=block",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "origin",
        "Expect-CT": "max-age=0",
        "Expires": "Mon, 13 Apr 2020 00:00:55 GMT",
        "Cache-Control": "max-age=31536000"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if verbose:
        print("[-] Retrieving the HTTP headers of the server...")

    headers = get_headers(server)

    if headers is not False:
        print(json.dumps(headers, indent=4))
    else:
        print("[X] URL {} is not valid!", file=sys.stderr)

    if verbose:
        print("[+] HTTP headers from {} retrieved".format(server))

    return True


if __name__ == '__main__':
    cmd_http_headers()

