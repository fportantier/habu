import json
import logging
import re
import sys
from pprint import pprint

import click
import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup


@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_webheaders(url, no_cache, verbose):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        requests_cache.install_cache('/tmp/habu_requests_cache')

    try:
        r = requests.get(url)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    pprint(dict(r.headers))

    # HSTS
    if not 'Strict-Transport-Security' in r.headers:
        print("NO HSTS")

    # X-Frame-Options
    if not 'X-Frame-Options' in r.headers:
        print("NO X-Frame-Options")

    # X-XSS-Protection
    if not 'X-XSS-Protection' in r.headers:
        print("NO X-XSS-Protection")

    if 'X-XSS-Protection' in r.headers and r.headers['X-XSS-Protection'] == 0:
        print("X-XSS-Protection disabled")

    if 'X-Content-Type-Options' not in r.headers:
        print("NO X-Content-Type-Options")

    if 'Content-Security-Policy' not in r.headers:
        print("NO Content-Security-Policy")

    if 'Server' in r.headers:
        print("Data divulgation by Server HTTP header")

    if 'X-Powered-By' in r.headers:
        print("Data divulgation by X-Powered-By HTTP header")

    if 'Public-Key-Pins' not in r.headers and 'Public-Key-Pins-Report-Only' not in r.headers:
        print("No Public-Key-Pins")


if __name__ == '__main__':
    cmd_webheaders()
