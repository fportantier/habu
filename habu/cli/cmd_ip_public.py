#!/usr/bin/env python3
import json

import click

from habu.lib.ip import get_public_ipv4, get_public_ipv6


@click.command()
@click.option('-4', '--ipv4', 'ipv4', is_flag=True, default=False, help='Print your public IPv4 address (default)')
@click.option('-6', '--ipv6', 'ipv6', is_flag=True, default=False, help='Print your public IPv6 address')
@click.option('-j', '--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
def cmd_ip_public(ipv4, ipv6, json_output):
    """Get the public IP address of the connection from https://api.ipify.org.

    Example:

    \b
    $ habu.ip.public
    80.219.53.185
    """

    result = {}

    if not ipv4 and not ipv6:
        ipv4 = True

    if ipv4:
        result['ipv4_address'] = get_public_ipv4()

    if ipv6:
        result['ipv6_address'] = get_public_ipv6()

    if json_output:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join([ v for v in result.values() ]))


if __name__ == '__main__':
    cmd_ip_public()
