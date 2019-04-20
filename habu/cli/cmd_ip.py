#!/usr/bin/env python3
import json

import click

from habu.lib.ip import get_external_ip


@click.command()
def cmd_ip():
    """Get the public IP address of the connection from https://api.ipify.org.

    Example:

    \b
    $ habu.ip
    {
        "ip_external": "80.219.53.185"
    }
    """
    answer = get_external_ip()

    print(json.dumps(answer, indent=4))

    return True


if __name__ == '__main__':
    cmd_ip()
