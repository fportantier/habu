#!/usr/bin/env python3

import json
import sys

import click

#from pathlib import Path

from habu.lib.loadcfg import loadcfg


@click.command()
@click.option('--show-keys', is_flag=True, default=False, help='Show also the key values')
@click.option('--option', nargs=2, help='Write to the config(KEY VALUE)')
def cmd_config(option, show_keys):
    """Show the current config.

    Note: By default, the options with 'KEY' in their name are shadowed.

    Example:

    \b
    $ habu.config
    {
        "DNS_SERVER": "8.8.8.8",
        "FERNET_KEY": "*************"
    }
    """

    habucfg = loadcfg()

    if not show_keys:
        for key in habucfg.keys():
            if 'KEY' in key:
                habucfg[key] = '*************'

    print(json.dumps(habucfg, indent=4, sort_keys=True))


if __name__ == '__main__':
    cmd_config()

