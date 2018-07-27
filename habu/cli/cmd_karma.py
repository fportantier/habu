#!/usr/bin/env python3

import ipaddress
import json
import logging
import socket
import sys

import click
import requests


@click.command()
@click.argument('host')
def cmd_karma(host):
    """Use the Karma service https://karma.securetia.com to check an IP
    against various Threat Intelligence / Reputation lists.

    \b
    $ habu.karma www.google.com
    www.google.com -> 64.233.190.99
    [
        "hphosts_fsa",
        "hphosts_psh",
        "hphosts_emd"
    ]

    Note: You can use the hostname or the IP of the host to query.
    """

    URL = 'https://karma.securetia.com/api/ip/'

    try:
        resolved = socket.gethostbyname(host)
    except Exception:
        logging.error('Invalid IP address or hostname')
        sys.exit(1)

    if host != resolved:
        print(host, '->', resolved, file=sys.stderr)

    r = requests.get(URL + resolved, headers={'Accept': 'application/json'})

    if r.status_code != 200:
        logging.error('HTTP Error code received: {}'.format(r.status_code))
        sys.exit(1)

    print(json.dumps(r.json(), indent=4))

if __name__ == '__main__':
    cmd_karma()
