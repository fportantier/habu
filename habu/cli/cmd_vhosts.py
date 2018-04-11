import json
import logging
import socket
import sys

import click

from habu.lib.vhosts import get_vhosts


@click.command()
@click.argument('host')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-p', 'pages', default=10, help='Pages count (Default: 10)')
@click.option('-f', 'first', default=1, help='First result to get (Default: 1)')
def cmd_vhosts(host, no_cache, pages, first):

    try:
        resolved = socket.gethostbyname(host)
    except Exception:
        logging.error('Invalid IP address or hostname')
        sys.exit(1)

    if host != resolved:
        print(host, '->', resolved, file=sys.stderr)

    vhosts = []

    for num in range(pages):
        vhosts += get_vhosts(resolved, no_cache=no_cache, first=first+num*10)

    vhosts = list(set(vhosts))

    print(json.dumps(vhosts, indent=4))

if __name__ == '__main__':
    cmd_vhosts()
