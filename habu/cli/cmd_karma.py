import ipaddress
#from habu.lib.ip2asn import ip2asn
import json
import logging
import socket
import sys

import click
import requests


@click.command()
@click.argument('host')
def cmd_karma(host):

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
