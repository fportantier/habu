#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.ip import get_internal_ip


@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
def cmd_ip_internal(verbose):
    """Get the local IP address(es) of the local interfaces.

    Example:

    \b
    $ habu.ip.internal
    {
      "lo": {
        "ipv4": [
          {
            "addr": "127.0.0.1",
            "netmask": "255.0.0.0",
            "peer": "127.0.0.1"
          }
        ],
        "link_layer": [
          {
            "addr": "00:00:00:00:00:00",
            "peer": "00:00:00:00:00:00"
          }
        ],
        "ipv6": [
          {
            "addr": "::1",
            "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128"
          }
        ]
      },
    ...
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Gathering NIC details...", file=sys.stderr)

    result = get_internal_ip()

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("[X] Unable to get detail about the interfaces")

    return True


if __name__ == '__main__':
    cmd_ip_internal()
