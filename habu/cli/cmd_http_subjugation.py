#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.http import get_headers, subjugation


@click.command()
@click.argument('server')
@click.option('-f', 'follow', is_flag=True, default=False,
              help='Follow the redirect.')
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
def cmd_http_subjugation(server, follow, verbose):
    """Retrieve the redirect location of a web server.

    Example:

    \b
    $ habu.http.subjugation http://duckduckgo.com
    {
        "redirect": "https://duckduckgo.com/"
    }

    $ habu.http.subjugation -f http://duckduckgo.com
    {
        "redirect": "https://duckduckgo.com/",
        "headers": {
            "Server": "nginx",
            "Date": "Wed, 17 Apr 2019 09:05:44 GMT",
            "Content-Type": "text/html; charset=UTF-8",
            "Connection": "keep-alive",
            "Vary": "Accept-Encoding",
            "ETag": "W/\"5cb6a8b8-1529\"",
            "Strict-Transport-Security": "max-age=31536000",
            "X-Frame-Options": "SAMEORIGIN",
            "Content-Security-Policy": "default-src https: blob: ...",
            "X-XSS-Protection": "1;mode=block",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "origin",
            "Expect-CT": "max-age=0",
            "Expires": "Wed, 17 Apr 2019 09:05:43 GMT",
            "Cache-Control": "no-cache",
            "Content-Encoding": "gzip"
        }
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if verbose:
        print("[-] Retrieving the HTTP location of the server...")

    location = subjugation(server)

    if location is not False:
        if follow:
            redirect = get_headers(location['redirect'])
            location['headers'] = redirect
            print(json.dumps(location, indent=4))
        else:
            print(json.dumps(location, indent=4))
    else:
        print("[X] URL {} is not valid!", file=sys.stderr)

    if verbose:
        print("[+] HTTP headers from {} retrieved".format(server))

    return True


if __name__ == '__main__':
    cmd_http_subjugation()
