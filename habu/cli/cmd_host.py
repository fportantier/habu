#!/usr/bin/env python3
import json
import logging
import sys

import click

from habu.lib.host import gather_details


@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
def cmd_host(verbose):
    """Collect information about the host where habu is running.

    Example:

    \b
    $ habu.host
    {
        "kernel": [
            "Linux",
            "demo123",
            "5.0.6-200.fc29.x86_64",
            "#1 SMP Wed Apr 3 15:09:51 UTC 2019",
            "x86_64",
            "x86_64"
        ],
        "distribution": [
            "Fedora",
            "29",
            "Twenty Nine"
        ],
        "libc": [
            "glibc",
            "2.2.5"
        ],
        "arch": "x86_64",
        "python_version": "3.7.3",
        "os_name": "Linux",
        "cpu": "x86_64",
        "static_hostname": "demo123",
        "fqdn": "demo123.lab.sierra"
    }
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Gather information about the host...", file=sys.stderr)

    result = gather_details()

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("[X] Unable to gather information")

    return True


if __name__ == '__main__':
    cmd_host()
