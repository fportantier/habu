#!/usr/bin/env python3

import json
import sys

import click

from pathlib import Path

from habu.lib.loadcfg import loadcfg


@click.command()
@click.argument('key')
def cmd_config_del(key):
    """Delete a KEY from the configuration.

    Note: By default, KEY is converted to uppercase.

    Example:

    \b
    $ habu.config.del DNS_SERVER
    """

    habucfg = loadcfg(environment=False)
    habucfg.pop(key.upper(), None)
    with Path('~/.habu.json').expanduser().open('w') as f:
        f.write(json.dumps(habucfg, indent=4, sort_keys=True))


if __name__ == '__main__':
    cmd_config_del()

