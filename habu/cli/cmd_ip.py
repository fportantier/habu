#!/usr/bin/env python3
import json

import click

from habu.lib.ip import get_external_ip


@click.command()
@click.option('-j', '--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
def cmd_ip(json_output):
    """Get the public IP address of the connection from https://api.ipify.org.

    Example:

    \b
    $ habu.ip
    80.219.53.185
    """
    answer = get_external_ip()

    if json_output:
        print(json.dumps(answer, indent=4))
    else:
        print(answer['ip_external'])

if __name__ == '__main__':
    cmd_ip()
