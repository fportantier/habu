"""Perform a forward lookup of a hostname."""
import json
import logging
import sys

import click

from habu.lib.dns import forward_lookup


@click.command()
@click.argument('hostname')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dns_forward_lookup(hostname, verbose):
    """Perform a forward lookup of a given hostname.

    Example:

    \b
    $ habu.dns.forward_lookup google.com
    {
        "ipv4": "172.217.168.46",
        "ipv6": "2a00:1450:400a:802::200e"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Looking up %s..." % hostname, file=sys.stderr)

    answer = forward_lookup(hostname)

    print(json.dumps(answer, indent=4))

    return True


if __name__ == '__main__':
    cmd_dns_forward_lookup()
