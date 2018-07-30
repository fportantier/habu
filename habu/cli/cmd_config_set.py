#!/usr/bin/env python3

import json
import sys

import click

from pathlib import Path

from habu.lib.loadcfg import loadcfg


@click.command()
@click.argument('key')
@click.argument('value')
def cmd_config_set(key, value):
    """Set VALUE to the config KEY.

    Note: By default, KEY is converted to uppercase.

    Example:

    \b
    $ habu.config.set DNS_SERVER 8.8.8.8
    """

    habucfg = loadcfg(environment=False)
    habucfg[key.upper()] = value
    with Path('~/.habu.json').expanduser().open('w') as f:
        f.write(json.dumps(habucfg, indent=4, sort_keys=True))


if __name__ == '__main__':
    cmd_config_set()

