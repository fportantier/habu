import json
import logging
import socket
import sys

import click

from habu.lib.ip2asn import ip2asn


@click.command()
@click.argument('ip')
def cmd_ip2asn(ip):

    try:
        resolved = socket.gethostbyname(ip)
    except Exception:
        logging.error('Invalid IP address or hostname')
        sys.exit(1)

    if ip != resolved:
        print(ip, '->', resolved, file=sys.stderr)

    data = ip2asn(resolved)
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    cmd_ip2asn()
